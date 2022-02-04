from typing import List, Union

import ujson
from pydantic import BaseModel

from tools import writeFile, deduplicate
from manifest import get, getAll, loadLocal
from data.seasons.d2_season_info import D2CalculatedSeason

loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")

# 赛季编号额外信息，前面几个赛季命名不规范
namedSeasonExceptions: dict[int, str] = {
    420: "outlaw",
    430: "forge",
    450: "opulence",
    460: "maverick",
}


def getSeasonID(season: int) -> str:
    """
    :说明: `getSeasonID`
    > 获取用于查询模组的赛季标识字符串

    :参数:
      * `season: int`: 赛季ID

    :返回:
    - `str`: 用于查询模组的赛季标识字符串
    """
    id = 420 + 10 * (season - 4)
    return f'enhancements.season_{namedSeasonExceptions.get(id, f"v{id}")}'


# 根据 plugCategoryIdentifier 名称的现有模式，使用假设预先生成一个表
seasonNumberByPlugCategoryIdentifier: dict[str, int] = {}
for season in range(4, D2CalculatedSeason + 1):
    seasonNumberByPlugCategoryIdentifier[getSeasonID(season)] = season


class ModSocketMetadata(BaseModel):
    season: int
    """这允许我们按时间顺序对模组进行排序以达到 LO 的目的"""

    tag: str
    """我们使用这两个来匹配搜索过滤器"""

    compatibleTags: List[str]
    """我们使用这两个来匹配搜索过滤器"""

    socketTypeHash: int
    """# 一个道具插口的 socketTypeHash 用于查找 ModSocketMetadata"""

    plugCategoryHashes: List[int]
    """
    模组本身并不指向它们的兼容插槽，它们只是有一个plugCategoryHash。
    一个socket指向一个socketType，它指的是多个plugCategoryHashes
    所以这里是一种更直接的方法，如果你有一个plugCategoryHash，无需进行数据表查找就可以找到ModSocketMetadata
    """

    compatiblePlugCategoryHashes: List[int]
    """哈希用于在加载管理器中更快地查找，它们直接对应于在单个模块中找到的信息"""

    emptyModSocketHash: int
    """这有助于我们查找空白的模组内容，以获取其图标/名称"""


seasonalPlugCategoryIdentifier = "enhancements.season_"


def seasonTagFromMod(item: dict) -> str:
    """
    :说明: `seasonTagFromMod`
    > 从模组名中获取赛季标识简称

    :参数:
      * `item: dict`: 模组的JSON字典数据

    :返回:
        - `str`: 赛季标识简称
    """
    tag = item["itemTypeDisplayName"]
    if tag.endswith("模组"):
        tag = tag[:-2]
    if tag.endswith("护甲"):
        tag = tag[:-2]
    if tag.endswith("突袭"):
        tag = tag[:-2]
    if tag.endswith("电池"):
        tag = tag[:-2]
    return tag


def getCompatibleTags(exampleArmorSocketEntry: dict) -> List[str]:
    """
    :说明: `getCompatibleTags`
    > 从示例道具插槽数据中获取所有可以插入这个插槽的模组

    :参数:
      * `exampleArmorSocketEntry: dict`: 示例的道具插槽数据

    :Exceptions:
      * ``: [description]

    :返回:
    - `List[str]`: [description]
    """
    if temp := exampleArmorSocketEntry.get("reusablePlugSetHash"):
        if temp := get("DestinyPlugSetDefinition", temp):
            return list(
                deduplicate(
                    [
                        seasonTagFromMod(plugItemHash)
                        for plugItem in temp["reusablePlugItems"]
                        if (
                            plugItemHash := get(
                                "DestinyInventoryItemDefinition",
                                plugItem.get("plugItemHash"),
                            )
                        )
                    ]
                )
            )
    raise ValueError(f"{exampleArmorSocketEntry} can get compatible tags")


def getEmptySeasonalModSocketsInfo(
    emptyModSocket: dict,
) -> Union[ModSocketMetadata, None]:
    """
    :说明: `getEmptySeasonalModSocketsInfo`
    > 获取空模组插槽相关信息

    :参数:
      * `emptyModSocket: dict`: 空模组插槽元数据

    :返回:
    - `Union(ModSocketMetadata, None)`: [description]
    """
    # 模组类型信息
    itemTypeDisplayName = emptyModSocket["itemTypeDisplayName"]

    # 与模组插槽相关的赛季编号
    season = seasonNumberByPlugCategoryIdentifier[
        emptyModSocket["plug"]["plugCategoryIdentifier"]
    ]

    # 赛季简称
    tag = seasonTagFromMod(emptyModSocket)

    # 具有此空插槽的示例装备
    if not (
        exampleArmorSocketEntry := findExampleSocketByEmptyModHash(
            emptyModSocket["hash"]
        )
    ):
        return None

    # 所有可以插入这个空模组插槽的模组
    compatibleTags = getCompatibleTags(exampleArmorSocketEntry) or []

    # 此空插槽的插槽类型
    socketTypeHash = exampleArmorSocketEntry["socketTypeHash"]

    # plugCategoryHashes 其原生插槽是这个
    plugCategoryHashes = list(
        deduplicate(
            [
                itemPlugCategoryHash
                for item in inventoryItems
                if item.get("itemTypeDisplayName") == itemTypeDisplayName
                and item.get("plug")
                and (itemPlugCategoryHash := item["plug"]["plugCategoryHash"])
            ]
        )
    )

    # 此 SocketType 支持的 plugCategoryHashes
    compatiblePlugCategoryHashes = [
        plugType["categoryHash"]
        for plugType in get("DestinySocketTypeDefinition", socketTypeHash)[
            "plugWhitelist"
        ]
    ]

    return ModSocketMetadata(
        season=season,
        tag=tag,
        compatibleTags=compatibleTags,
        socketTypeHash=socketTypeHash,
        plugCategoryHashes=plugCategoryHashes,
        compatiblePlugCategoryHashes=compatiblePlugCategoryHashes,
        emptyModSocketHash=emptyModSocket["hash"],
    )


def findExampleSocketByEmptyModHash(emptyModSocketHash: int) -> Union[dict, None]:
    """
    :说明: `findExampleSocketByEmptyModHash`
    > 获取空模组插槽的示例装备的插槽数据

    :参数:
      * `emptyModSocketHash: int`: 空模组插槽的哈希

    :返回:
    - `Union[dict, None]`: 示例装备的插槽数据, 未查询到则为 None
    """
    targetInventoryItems = [
        i
        for i in inventoryItems
        if (sockets := i.get("sockets"))
        and any(
            [
                j
                for j in sockets["socketEntries"]
                if j["singleInitialItemHash"] == emptyModSocketHash
            ]
        )
    ]
    if targetInventoryItems:
        return [
            j
            for j in targetInventoryItems[0]["sockets"]["socketEntries"]
            if j["singleInitialItemHash"] == emptyModSocketHash
        ][0]
    else:
        return None


# 查找名称为空模组插槽的插槽信息
emptySeasonalModSockets = [
    i
    for i in inventoryItems
    if i["displayProperties"]["name"] == "空模组插槽"
    and (plug := i.get("plug"))
    and plug["plugCategoryIdentifier"].startswith(seasonalPlugCategoryIdentifier)
]

# 按 hash 对空模组插槽排序
emptySeasonalModSockets.sort(key=lambda x: x["hash"])

modMetadatas: List[ModSocketMetadata] = [
    modMetadata
    for emptyModSocket in emptySeasonalModSockets
    if (modMetadata := getEmptySeasonalModSocketsInfo(emptyModSocket))
]


modMetadatas.sort(key=lambda x: x.season)
seasonNameOrder = [i.tag for i in modMetadatas]


def sortCompatibleTags(key: str) -> int:
    """
    :说明: `sortCompatibleTags`
    > sortCompatibleTags 排序取 key

    :参数:
      * `key: str`: sortCompatibleTag

    :返回:
    - `int`: 返回元素的位置, 未查询到则返回 -1
    """
    try:
        return seasonNameOrder.index(key)
    except ValueError:
        return -1


# 对字段进行排序
for m in modMetadatas:
    m.compatiblePlugCategoryHashes.sort(key=str)
    m.plugCategoryHashes.sort(key=str)
    m.compatibleTags.sort(key=sortCompatibleTags)

# 将 modMetadatas 转为字符串
modMetadatasStr = ujson.dumps(
    [i.dict() for i in modMetadatas], ensure_ascii=False, indent=4
)


pretty = """from pydantic import BaseModel

from typing import List


class ModSocketMetadata(BaseModel):
    season: int
    \"\"\"这允许我们按时间顺序对模组进行排序以达到 LO 的目的\"\"\"

    tag: str
    \"\"\"我们使用这两个来匹配搜索过滤器\"\"\"

    compatibleTags: List[str]
    \"\"\"我们使用这两个来匹配搜索过滤器\"\"\"

    socketTypeHash: int
    \"\"\"# 一个道具插口的 socketTypeHash 用于查找 ModSocketMetadata\"\"\"

    plugCategoryHashes: List[int]
    \"\"\"
    模组本身并不指向它们的兼容插槽，它们只是有一个plugCategoryHash。
    一个socket指向一个socketType，它指的是多个plugCategoryHashes
    所以这里是一种更直接的方法，如果你有一个plugCategoryHash，无需进行数据表查找就可以找到ModSocketMetadata
    \"\"\"

    compatiblePlugCategoryHashes: List[int]
    \"\"\"哈希用于在加载管理器中更快地查找，它们直接对应于在单个模块中找到的信息\"\"\"

    emptyModSocketHash: int
    \"\"\"这有助于我们查找空白的模组内容，以获取其图标/名称\"\"\"
    """


pretty += "\n\nmodMetadatasList = " + modMetadatasStr
pretty += "\n\nmodMetadatas = [ModSocketMetadata(**i) for i in modMetadatasList]"

writeFile("./output/specialty_modslot_metadata.py", pretty)
cc = 0
