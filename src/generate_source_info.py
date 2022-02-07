from typing import List, Union, Optional

import ujson
from pydantic import BaseModel

from log import logger
from tools import annotate, writeFile, sortObject, dedupeAndSortArray
from manifest import get, getAll, loadLocal
from data.generated_enums import ItemCategoryHashes


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
            if [i.lower() for i in includes if i in sourceString.lower()]
        ]
    if excludes:
        # 排除 excludes
        sourceStrings = [
            sourceString
            for sourceString in sourceStrings
            if not [i.lower() for i in excludes if i in sourceString.lower()]
        ]
    # 只返回匹配到的 sourceHash 列表
    return [
        sourceHash
        for sourceHash in haystack.keys()
        if haystack[sourceHash] in sourceStrings
    ]


categories = Categories.parse_file("./data/sources/categories_translated.json")

loadLocal()

allInventoryItems = getAll("DestinyInventoryItemDefinition")
allCollectibles = getAll("DestinyCollectibleDefinition")
allPresentationNodes = getAll("DestinyPresentationNodeDefinition")

# 这只是一个 hash-to-sourceString 转换表，since none exists (因为不存在这样的表)。
sourceStringsByHash: dict[int, str] = {}
unassignedSourceStringsByHash: dict[int, str] = {}
allSources: List[int] = []
assignedSources: List[int] = []
unassignedSources: List[int] = []

for collectible in allCollectibles:
    sourceName = (
        sourceString
        if (sourceString := collectible.get("sourceString"))
        else collectible["displayProperties"]["description"]
    )
    # 仅添加具有现有哈希的源（例如，没有分类项目）
    if hash := collectible.get("sourceHash"):
        # 这里对原项目做了修改，CN包里面出现了一个 sourceName 为空的项目，所以要做额外的过滤
        if sourceName:
            sourceStringsByHash[hash] = sourceName
        allSources.append(hash)

sourceStringsByHash = sortObject(sourceStringsByHash)
writeFile("./output/sources.json", sourceStringsByHash)


class D2SourceInfo(BaseModel):
    itemHashes: List[int]
    sourceHashes: List[int]
    searchString: List[str]


sourcesInfo: dict[int, str] = {}
D2Sources: dict[str, D2SourceInfo] = {}

# 由 manifest collectibles 构建 sourcesInfo
for collectible in allCollectibles:
    if collectible.get("sourceHash"):
        sourcesInfo[collectible["sourceHash"]] = collectible["sourceString"]

# 从 categories.json 添加手动源字符串
for sourceHash, sourceString in categories.exceptions:
    sourcesInfo[int(sourceHash)] = sourceString

# 循环进行分类
for sourceTag, matchRule in categories.sources.items():
    # 这是经过 includes 和 excludes 过滤后的 sourceHash 列表
    sourceHashes = applySourceStringRules(sourcesInfo, matchRule)
    assignedSources.extend([*sourceHashes])
    searchString: List[str] = []
    # 准备好 searchString
    if matchRule.searchString:
        searchString = [*matchRule.searchString]

    # 值得注意的是我们的规则之一是否已失效
    if not len(sourceHashes):
        logger.warning(f"no matching sources for {sourceTag}: {matchRule.dict()}")

    # 与此 sourceTag 对应的项目哈希
    itemHashes: List[int] = []

    # 按名称查找任何指定的单个项目，并添加它们的 hash
    if items := matchRule.items:
        for itemNameOrHash in items:
            includedItemHashes = [
                i["hash"]
                for i in allInventoryItems
                if ItemCategoryHashes.样品模型 not in i.get("itemCategoryHashes", [])
                and ItemCategoryHashes.任务步骤 not in i.get("itemCategoryHashes", [])
                and (
                    itemNameOrHash == str(i["hash"])
                    or i.get("displayProperties", {"name": ""})["name"] == itemNameOrHash
                )
            ]
            itemHashes.extend(includedItemHashes)
    # 如果提供了任何 presentation nodes name 或 hash，
    # 获取他们包含的装备，然后添加它们
    if presentationNodes := matchRule.presentationNodes:
        foundPresentationNodes = [
            p
            for p in allPresentationNodes
            if str(p["hash"]) in presentationNodes
            or p.get("displayProperties", {"name": ""})["name"] in presentationNodes
        ]
        for foundPresentationNode in foundPresentationNodes:
            for collectible in foundPresentationNode["children"]["collectibles"]:
                if childItem := get(
                    "DestinyCollectibleDefinition", collectible.get("collectibleHash")
                ):
                    if childItemHash := childItem.get("itemHash"):
                        itemHashes.append(childItemHash)

    # 添加所有元素后排序和去重
    itemHashes = dedupeAndSortArray(itemHashes)

    # 将结果添加到输出表中
    D2Sources[sourceTag] = D2SourceInfo(
        itemHashes=itemHashes,
        sourceHashes=sourceHashes,
        searchString=searchString,
    )

    # 最后添加别名并复制信息
    if alias := matchRule.alias:
        D2Sources[alias] = D2Sources[sourceTag]

# 删除要忽略的来源
D2Sources.pop("ignore", None)


D2SourcesSorted: dict[str, D2SourceInfo] = sortObject(D2Sources)
for SourceInfo in D2SourcesSorted.values():
    SourceInfo.itemHashes.sort(key=str)
    SourceInfo.sourceHashes.sort(key=str)
    SourceInfo.searchString.sort(key=str)

D2SourcesStringified = {k: v.dict() for k, v in D2SourcesSorted.items()}

pretty = f"""from typing import List

from pydantic import BaseModel


class D2SourceInfo(BaseModel):
    itemHashes: List[int]
    sourceHashes: List[int]
    searchString: List[str]


D2SourcesJson: dict[str, dict] = {ujson.dumps(D2SourcesStringified, ensure_ascii=False, indent=4)}

"""
pretty += "D2Sources: dict[str, D2SourceInfo] = {\nk: D2SourceInfo.parse_obj(v) for k, v in D2SourcesJson.items()\n}"

annotated = annotate(pretty, sourcesInfo)
writeFile("./output/source_info.py", annotated)

unassignedSources = [i for i in allSources if i not in assignedSources]

for hash in unassignedSources:
    sourceList = [i for i in allCollectibles if i["hash"] == hash]
    if sourceList:
        source = sourceList[0]
        sourceName = (
            name
            if (name := source.get("sourceString"))
            else (
                source.get("displayProperties", {"description": ""}.get("description"))
                or ""
            )
        )
        unassignedSourceStringsByHash[hash] = sourceName
    else:
        logger.warning(f"no sourceName found for {hash}")

writeFile("./data/sources/unassigned.json", unassignedSourceStringsByHash)
