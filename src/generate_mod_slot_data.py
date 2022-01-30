from typing import List

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


def getSeasonID(season: int):
    id = 420 + 10 * (season - 4)
    return f'enhancements.season_{namedSeasonExceptions.get(id, f"v{id}")}'


# 根据 plugCategoryIdentifier 名称的现有模式，使用假设预先生成一个表
seasonNumberByPlugCategoryIdentifier: dict[str, int] = {}
for season in range(4, D2CalculatedSeason + 1):
    seasonNumberByPlugCategoryIdentifier[getSeasonID(season)] = season


class ModSocketMetadata(BaseModel):
    # 这允许我们按时间顺序对模组进行排序以达到 LO 的目的
    season: int
    # 我们使用这两个来匹配搜索过滤器
    tag: str
    compatibleTags: List[str]
    # 一个道具插口的 socketTypeHash 用于查找 ModSocketMetadata
    socketTypeHash: int
    """
    模组本身并不指向它们的兼容插槽，它们只是有一个plugCategoryHash。
    一个socket指向一个socketType，它指的是多个plugCategoryHashes
    所以这里是一种更直接的方法，如果你有一个plugCategoryHash，无需进行数据表查找就可以找到ModSocketMetadata
    """
    plugCategoryHashes: List[int]
    # 哈希用于在加载管理器中更快地查找，它们直接对应于在单个模块中找到的信息
    compatiblePlugCategoryHashes: List[int]
    # 这有助于我们查找空白的模组内容，以获取其图标/名称
    emptyModSocketHash: int


seasonalPlugCategoryIdentifier = "enhancements.season_"


def seasonTagFromMod(item: dict) -> str:
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


def getCompatibleTags(exampleArmorSocketEntry: dict):
    temp = exampleArmorSocketEntry.get("reusablePlugSetHash")
    if temp:
        temp = get("DestinyPlugSetDefinition", temp)
        if temp:
            return list(
                deduplicate(
                    [
                        seasonTagFromMod(
                            get(
                                "DestinyInventoryItemDefinition",
                                plugItem["plugItemHash"],
                            )
                        )
                        for plugItem in temp["reusablePlugItems"]
                        if get(
                            "DestinyInventoryItemDefinition",
                            plugItem.get("plugItemHash"),
                        )
                    ]
                )
            )


def getEmptySeasonalModSocketsInfo(emptyModSocket: dict):
    # 模组类型信息
    itemTypeDisplayName = emptyModSocket["itemTypeDisplayName"]

    # 与模组插槽相关的赛季编号
    season = seasonNumberByPlugCategoryIdentifier[
        emptyModSocket["plug"]["plugCategoryIdentifier"]
    ]

    # 赛季简称
    tag = seasonTagFromMod(emptyModSocket)

    # 具有此空插槽的示例装备
    exampleArmorSocketEntry = findExampleSocketByEmptyModHash(emptyModSocket["hash"])
    if not exampleArmorSocketEntry:
        return

    # 所有可以插入这个空模组插槽的模组
    compatibleTags = getCompatibleTags(exampleArmorSocketEntry) or []

    # 此空插槽的插槽类型
    socketTypeHash = exampleArmorSocketEntry["socketTypeHash"]

    # plugCategoryHashes 其原生插槽是这个
    plugCategoryHashes = list(
        deduplicate(
            [
                item["plug"]["plugCategoryHash"]
                for item in inventoryItems
                if item.get("itemTypeDisplayName") == itemTypeDisplayName
                if item.get("plug") and item["plug"]["plugCategoryHash"]
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


def findExampleSocketByEmptyModHash(emptyModSocketHash: int):
    targetInventoryItems = [
        i
        for i in inventoryItems
        if i.get("sockets")
        and any(
            [
                j
                for j in i["sockets"]["socketEntries"]
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
    and i.get("plug")
    and i["plug"]["plugCategoryIdentifier"].startswith(seasonalPlugCategoryIdentifier)
]

# 按 hash 对空模组插槽排序
emptySeasonalModSockets.sort(key=lambda x: x["hash"])

modMetadatas: List[ModSocketMetadata] = [
    i
    for i in [
        getEmptySeasonalModSocketsInfo(emptyModSocket)
        for emptyModSocket in emptySeasonalModSockets
    ]
    if i
]

modMetadatas.sort(key=lambda x: x.season)
seasonNameOrder = [i.tag for i in modMetadatas]


def sortCompatibleTags(key: str) -> int:
    try:
        return seasonNameOrder.index(key)
    except ValueError:
        return -1


for m in modMetadatas:
    m.compatiblePlugCategoryHashes.sort()
    m.plugCategoryHashes.sort()
    m.compatibleTags.sort(key=sortCompatibleTags)


modMetadatasStr = ujson.dumps(
    [i.dict() for i in modMetadatas], ensure_ascii=False, indent=4
)


pretty = """from pydantic import BaseModel
from typing import List

class ModSocketMetadata(BaseModel):
    # 这允许我们按时间顺序对模组进行排序以达到 LO 的目的
    season: int
    # 我们使用这两个来匹配搜索过滤器
    tag: str
    compatibleTags: List[str]
    # 一个道具插口的 socketTypeHash 用于查找 ModSocketMetadata
    socketTypeHash: int
    \"\"\"
    模组本身并不指向它们的兼容插槽，它们只是有一个plugCategoryHash。
    一个socket指向一个socketType，它指的是多个plugCategoryHashes
    所以这里是一种更直接的方法，如果你有一个plugCategoryHash，无需进行数据表查找就可以找到ModSocketMetadata
    \"\"\"
    plugCategoryHashes: List[int]
    # 哈希用于在加载管理器中更快地查找，它们直接对应于在单个模块中找到的信息
    compatiblePlugCategoryHashes: List[int]
    # 这有助于我们查找空白的模组内容，以获取其图标/名称
    emptyModSocketHash: int
    """
pretty += "\n\nmodMetadatasList = " + modMetadatasStr
pretty += "\n\nmodMetadatas = [ModSocketMetadata(**i) for i in modMetadatasList]"

writeFile("./output/specialty_modslot_metadata.py", pretty)
cc = 0
