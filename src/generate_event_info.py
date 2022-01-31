import re
import json
from typing import Any

from tools import writeFile
from manifest import get, getAll, loadLocal
from data.generated_enums import ItemCategoryHashes

loadLocal()


def loadJson(file: str):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


crimsondays: list[int] = loadJson("./data/events/crimsondays.json")
dawning: list[int] = loadJson("./data/events/dawning.json")
eventDenyList: list[int] = loadJson("./data/events/deny-list.json")
fotl: list[int] = loadJson("./data/events/fotl.json")
games: list[int] = loadJson("./data/events/guardian_games.json")
revelry: list[int] = loadJson("./data/events/revelry.json")
solstice: list[int] = loadJson("./data/events/solstice.json")
all_sources: dict[int, str] = loadJson("./output/sources.json")

inventoryItems = getAll("DestinyInventoryItemDefinition")
_vendors: dict = getAll("DestinyVendorDefinition")  # type: ignore

eventInfo: dict[int, dict[str, Any]] = {
    1: {"name": "曙光节", "shortname": "曙光节", "sources": [], "engram": []},
    2: {"name": "血色浪漫", "shortname": "血色浪漫", "sources": [], "engram": []},
    3: {"name": "至日英雄", "shortname": "至日", "sources": [], "engram": []},
    4: {"name": "英灵日", "shortname": "英灵日", "sources": [], "engram": []},
    5: {"name": "狂欢季节", "shortname": "狂欢", "sources": [], "engram": []},
    6: {"name": "守护者游戏", "shortname": "游戏", "sources": [], "engram": []},
}

# * 将每个活动的来源放入eventInfo中
for source in all_sources:
    for num, event in eventInfo.items():
        if event["name"] in all_sources[source]:
            event["sources"].append(int(source))

sourcedItems: list[int] = [y for x in eventInfo.values() for y in x["sources"]]

eventItemsLists: dict[str, int] = {}

itemHashDenyList = eventDenyList

itemHashAllowList: dict[int, list[int]] = {
    1: dawning,
    2: crimsondays,
    3: solstice,
    4: fotl,
    5: revelry,
    6: games,
}

events: dict[str, int] = {
    "曙光节": 1,
    "血色浪漫": 2,
    "至日": 3,
    "英灵日": 4,
    "狂欢季节": 5,
    "守护者游戏": 6,
}

# * 这些类的东西不要包含进去
categoryDenyList = [
    ItemCategoryHashes.任务步骤,
    ItemCategoryHashes.货币,
    ItemCategoryHashes.记忆水晶,
    ItemCategoryHashes.材料,
    ItemCategoryHashes.赛雀模组,
    ItemCategoryHashes.包裹,
    ItemCategoryHashes.护甲模组皮肤,
    ItemCategoryHashes.悬赏,
    ItemCategoryHashes.藏宝图,
    ItemCategoryHashes.样品模型,
]

eventDetector = re.compile(r"|".join(events.keys()))

for item in inventoryItems:
    itemDescription = item["displayProperties"]["description"]
    if not (des := re.findall(eventDetector, itemDescription)):
        continue
    eventName = des[0]
    eventID = events[eventName]
    collectHash = get("DestinyCollectibleDefinition", item["collectibleHash"])
    collectibleHash = collectHash["sourceHash"] if collectHash else -99999999

    if not item.get("displayProperties"):
        continue

    if not item["itemCategoryHashes"]:
        continue

    # * 跳过物品分类当
    if (
        collectibleHash in sourcedItems  # * 如果这个物品已经在活动中时
        or item["itemCategoryHashes"] in categoryDenyList  # * 如果这个物品的分类在黑名单中
        or item["hash"] in itemHashDenyList  # * 如果这个物品在黑名单中
        or item["displayProperties"]["name"] == ""  # * 如果这个物品的名字为空
        or item.get("gearset")  # * 如果这个物品是套装的一部分
        or not item["itemCategoryHashes"]  # * 如果这个物品的分类为0
    ):
        continue

    eventItemsLists[item["hash"]] = eventID

vendors: dict[int, dict[str, Any]] = {}

for hash, vendor in _vendors.items():
    # * 缺少基础数据
    if not (dP := vendor.get("displayProperties")):
        continue
    if not dP["description"]:
        continue

    # * 不是记忆水晶
    if "记忆水晶" not in dP["name"]:
        continue

    # * 包含活动名字
    if re.findall(eventDetector, dP["description"]):
        vendors[hash] = vendor
        continue

    # * 如果到这都不是活动记忆水晶的话，就将其放入黑名单中
    itemHashDenyList.append(hash)

for hash, engram in vendors.items():
    eventID = events[
        re.findall(eventDetector, engram["displayProperties"]["description"])[0]
    ]
    eventInfo[eventID]["engram"].append(hash)

    for listItem in engram["itemList"]:
        item = get("DestinyInventoryItemDefinition", listItem["itemHash"])

        collectHash = get("DestinyCollectibleDefinition", item["collectibleHash"])
        collectibleHash = collectHash["sourceHash"] if collectHash else -99999999
        # * 跳过此物品当
        if (
            # * 已经有活动来源了
            collectibleHash in sourcedItems
            # * 不是要包含的类别
            or (
                item["itemCategoryHashes"]
                and ((hash in item["itemCategoryHashes"]) for hash in categoryDenyList)
            )
            # * 是另外的记忆水晶
            or item["hash"] in itemHashDenyList
            # * 没有名字
            or not (dP := item.get("displayProperties"))
            or not dP["name"]
            # * 是套装的一部分
            or item.get("gearset")
            # * 没有分类
            or not item["itemCategoryHashes"]
        ):
            continue

        eventItemsLists[item["hash"]] = eventID
