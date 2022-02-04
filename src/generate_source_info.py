from typing import List, Union, Optional

from pydantic import BaseModel

from tools import writeFile
from manifest import getAll, loadLocal


class CategoriesSources(BaseModel):
    """
    :说明: `CategoriesSources`
    > 对来源信息的筛选设定
    """

    includes: List[str]
    """字符串列表， 如果一个来源描述包含其中之一，它可能指的是这个 sourceTag"""

    excludes: Optional[List[str]]
    """字符串列表，如果一个来源描述包含其中之一, 他不可能指这个 sourceTag"""

    items: Optional[List[Union[str, int]]]
    """一个包含来源英文名或来源 hash 的列表"""

    alias: Optional[str]
    """将此类别复制到另一个 sourceTag"""

    presentationNodes: Optional[List[Union[str, int]]]
    """
    presentationNodes 包含一个 items (Collections) 的集合,
    我们将通过名称或哈希找到 presentationNodes 并将他们的子项目添加到 来源中
    """

    searchString: Optional[List[str]]


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


categories = Categories.parse_file("./data/sources/categories.json")

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

# 查看分类规则的循环
cc = 0
