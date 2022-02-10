from typing import List, Union, Optional

import ujson
from pydantic import BaseModel

from log import logger
from tools import annotate, writeFile, sortObject, dedupeAndSortArray
from manifest import getAll, loadLocal


class CategoriesSources(BaseModel):
    """
    :说明: `CategoriesSources`
    > 对来源信息的筛选设定
    """

    includes: Optional[List[str]] = []
    """字符串列表， 如果一个来源描述包含其中之一，它可能指的是这个 sourceTag"""

    excludes: Optional[List[str]] = []
    """字符串列表，如果一个来源描述包含其中之一, 他不可能指这个 sourceTag"""

    items: Optional[List[Union[str, int]]] = []
    """一个包含来源英文名或来源 hash 的列表"""

    alias: Optional[str] = ""
    """将此类别复制到另一个 sourceTag"""

    presentationNodes: Optional[List[Union[str, int]]] = []
    """
    presentationNodes 包含一个 items (Collections) 的集合,
    我们将通过名称或哈希找到 presentationNodes 并将他们的子项目添加到 来源中
    """

    searchString: Optional[List[str]] = []


class Categories(BaseModel):
    """
    :说明: `Categories`
    > 来源类别数据类
    """

    sources: dict[
        str,  # 一个 sourceTag, i.e. "adventures" or "deadorbit" or "zavala" or "crucible"
        CategoriesSources,
    ]

    exceptions: List[List[str]]


# 检查 haystack 值之间的 sourceStringRules 匹配
# 并返回匹配值的键
# 这会输出一个 sourceHashes 列表
def applySourceStringRules(
    haystack: dict[int, str], sourceStringRules: CategoriesSources
) -> List[int]:
    includes, excludes = sourceStringRules.includes, sourceStringRules.excludes
    sourceStrings = list(haystack.values())
    if includes:
        # 包含 includes
        sourceStrings = [
            sourceString
            for sourceString in sourceStrings
            if [i for i in includes if i.lower() in sourceString.lower()]
        ]
    if excludes:
        # 排除 excludes
        sourceStrings = [
            sourceString
            for sourceString in sourceStrings
            if not [i for i in excludes if i.lower() in sourceString.lower()]
        ]
    # 只返回匹配到的 sourceHash 列表
    return [
        sourceHash
        for sourceHash in haystack.keys()
        if haystack[sourceHash] in sourceStrings
    ]


categories = Categories.parse_file("./data/sources/categories.json")

logger.info("Generating missing collectible info...没有可收集哈希的库存物品信息")
loadLocal(language="en")

inventoryItems = getAll("DestinyInventoryItemDefinition", language="en")
collectibles = getAll("DestinyCollectibleDefinition", language="en")
hashToMissingCollectibleHash: dict[str, int] = {}

# 没有可收集哈希的库存物品
nonCollectibleItems = [
    item for item in inventoryItems if not item.get("collectibleHash")
]

# 有可收集哈希的库存物品
collectibleItems = [item for item in inventoryItems if item.get("collectibleHash")]


def stringifySortCompare(arr1: List[int], arr2: List[int]):
    return sorted(arr1) == sorted(arr2)


for collectibleItem in collectibleItems:
    itemsWithSameName = [
        nonCollectibleItem
        for nonCollectibleItem in nonCollectibleItems
        if collectibleItem["displayProperties"].get("name")
        and collectibleItem["displayProperties"]["name"]
        == nonCollectibleItem["displayProperties"]["name"]
        and stringifySortCompare(
            collectibleItem.get("itemCategoryHashes", []),
            nonCollectibleItem.get("itemCategoryHashes", []),
        )
    ]

    for nonCollectibleItem in itemsWithSameName:
        collectibleinfo = [
            sourceHash
            for collectible in collectibles
            if collectibleItem["collectibleHash"] == collectible["hash"]
            and (sourceHash := collectible.get("sourceHash"))
        ][0]
        hashToMissingCollectibleHash[nonCollectibleItem["hash"]] = collectibleinfo

hashToMissingCollectibleHash = sortObject(hashToMissingCollectibleHash)
sourcesInfo: dict[int, str] = {}
D2Sources: dict[str, List[int]] = {}
newSourceInfo: dict[str, List[int]] = {}

for collectible in collectibles:
    if collectible.get("sourceHash"):
        sourcesInfo[collectible["sourceHash"]] = collectible.get("sourceString")


# 循环进行分类
for sourceTag, matchRule in categories.sources.items():
    if sourceTag == "ignore":
        continue
    D2Sources[sourceTag] = applySourceStringRules(sourcesInfo, matchRule)

    if not len(D2Sources[sourceTag]):
        logger.warning(f"no matching sources for {sourceTag}: {matchRule.dict()}")

    sourceHashes = D2Sources[sourceTag]
    newSourceInfo[sourceTag] = newSourceInfo.get(sourceTag) or []
    for hash, sourceHash in hashToMissingCollectibleHash.items():
        if sourceHash in sourceHashes:
            newSourceInfo[sourceTag].append(int(hash))

    newSourceInfo[sourceTag] = dedupeAndSortArray(newSourceInfo[sourceTag])

    if alias := matchRule.alias:
        newSourceInfo[alias] = newSourceInfo[sourceTag]

D2SourcesSorted = sortObject(newSourceInfo)

pretty = f"""missingSources = {ujson.dumps(D2SourcesSorted, ensure_ascii=False, indent=4)}
"""
# 供添加注释的中文包加载
loadLocal()
annotated = annotate(pretty, sourcesInfo)

# 没有可收集哈希的库存物品进行分类
writeFile("./output/missing_source_info.py", annotated)
logger.success("writeFile ./output/missing_source_info.py")
logger.info("Generating missing collectible info... Done")
