import re
import json
from typing import Any, List

from log import logger
from tools import writeFile, sortObject
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
vendors: list = getAll("DestinyVendorDefinition")  # type: ignore

eventInfo: dict[int, dict[str, Any]] = {
    1: {"name": "曙光节", "shortname": "曙光节", "sources": [], "engram": []},
    2: {"name": "血色浪漫", "shortname": "血色浪漫", "sources": [], "engram": []},
    3: {"name": "至日英雄", "shortname": "至日", "sources": [], "engram": []},
    4: {"name": "英灵日", "shortname": "英灵日", "sources": [], "engram": []},
    5: {"name": "狂欢季节", "shortname": "欢庆", "sources": [], "engram": []},
    6: {"name": "守护者游戏", "shortname": "游戏", "sources": [], "engram": []},
}

# * 将每个活动的来源放入eventInfo中
for source in all_sources:
    for num, event in eventInfo.items():
        if event["name"] in all_sources[source]:
            event["sources"].append(int(source))

sourcedItems: list[int] = [y for x in eventInfo.values() for y in x["sources"]]

eventItemsLists: dict[int, int] = {}

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
    "曙光": 1,
    "血色浪漫日": 2,
    "至日": 3,
    "英灵日": 4,
    "欢庆": 5,
    "狂欢": 5,
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
    itemName = item["displayProperties"]["name"]
    if not (des := re.findall(eventDetector, item["displayProperties"]["description"])):
        continue
    eventName = des[0]
    eventID = events[eventName]

    if not item.get("collectibleHash"):
        collectibleHash = -99999999
    else:
        collectHash = get("DestinyCollectibleDefinition", item["collectibleHash"])
        collectibleHash = collectHash["sourceHash"] if collectHash else -99999999

    # * 跳过物品分类当
    if (
        collectibleHash in sourcedItems  # * 如果这个物品已经在活动中时
        or len(item.get("itemCategoryHashes", [])) == 0  # * 如果这个物品没有分类时
        or any(
            hash in categoryDenyList for hash in item["itemCategoryHashes"]
        )  # * 如果这个物品的分类在黑名单中
        or item["hash"] in itemHashDenyList  # * 如果这个物品在黑名单中
        or not item["displayProperties"]["name"]  # * 如果这个物品的名字为空
        or item.get("gearset")  # * 如果这个物品是套装的一部分
    ):
        continue

    eventItemsLists[item["hash"]] = eventID
    logger.info(
        f"{itemName}[{item['hash']}]\t{eventName}\t{item['displayProperties']['description']}"
    )

engramVendor: List[dict] = []

# 对记忆水晶添加 血色浪漫 为键
events["血色浪漫"] = 2
eventDetector = re.compile(r"|".join([eventDetector.pattern, "血色浪漫"]))
for vendor in vendors:

    if (not vendor["displayProperties"]["description"]) or "记忆水晶" not in vendor[
        "displayProperties"
    ]["name"]:
        continue

    hash = vendor["hash"]
    # * 包含活动名字
    if re.findall(eventDetector, vendor["displayProperties"]["description"]):
        engramVendor.append(vendor)
        continue

    # * 如果到这都不是活动记忆水晶的话，就将其放入黑名单中
    itemHashDenyList.extend([item["itemHash"] for item in vendor.get("itemList", [])])

for engram in engramVendor:
    eventID = events[
        re.findall(
            eventDetector,
            engram["displayProperties"]["description"],
        )[0]
    ]
    eventInfo[eventID]["engram"].append(engram["hash"])

    for listItem in engram["itemList"]:
        item = get("DestinyInventoryItemDefinition", listItem["itemHash"])

        if not item.get("collectibleHash"):
            collectibleHash = -99999999
        else:
            collectHash = get("DestinyCollectibleDefinition", item["collectibleHash"])
            collectibleHash = collectHash["sourceHash"] if collectHash else -99999999
        # * 跳过此物品当
        if (
            collectibleHash in sourcedItems  # 已经有活动来源了
            or len(item.get("itemCategoryHashes", [])) == 0  # 没有分类
            or any(
                hash in categoryDenyList for hash in item["itemCategoryHashes"]
            )  # 如果这个物品的分类在黑名单中
            or item["hash"] in itemHashDenyList  # 是其他记忆水晶
            or not item["displayProperties"]["name"]  # 没有名字
            or item.get("gearset")  # 是套装的一部分
        ):
            continue
        eventItemsLists[item["hash"]] = eventID

# 将不能自动加入的物品放入
for eventID, itemList in itemHashAllowList.items():
    for itemHash in itemList:
        eventItemsLists[itemHash] = eventID

eventItemsLists = sortObject(eventItemsLists)

writeFile("./output/events.json", eventItemsLists)

# * 生成 d2_event_info.py
D2EventEnum = ""
D2EventPredicateLookup = ""
D2SourcesToEvent = ""
D2EventInfo = ""

for eventNumber, eventAttrs in eventInfo.items():
    enumName = eventAttrs["shortname"]
    D2EventEnum += f"    {enumName} = {eventNumber}\n"

    D2EventInfo += f"""    {eventNumber}: {{
        \"name\": \"{eventAttrs["name"]}\",
        \"shortname\": \"{eventAttrs["shortname"]}\",
        \"sources\": {eventAttrs["sources"]},
        \"engram\": {eventAttrs["engram"]},
    }},
"""

    D2EventPredicateLookup += (
        f"    \"{eventAttrs['shortname']}\": D2EventEnum.{enumName},\n"
    )

    for source in eventAttrs["sources"]:
        D2SourcesToEvent += f"    {source}: D2EventEnum.{enumName},\n"

eventData = f"""from enum import IntEnum


class D2EventEnum(IntEnum):
{D2EventEnum}

D2EventInfo = {{
{D2EventInfo}
}}

D2EventPredicateLookup = {{
{D2EventPredicateLookup}
}}

D2SourcesToEvent = {{
{D2SourcesToEvent}
}}"""


writeFile("./output/d2_event_info.py", eventData)
