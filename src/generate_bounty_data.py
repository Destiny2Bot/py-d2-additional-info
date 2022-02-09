import re
from typing import List

from bungieapi.generated.components.schemas.destiny.definitions import (
    DestinyInventoryItemDefinition,
)

from log import logger
from tools import writeFile
from manifest import get, getAll, loadLocal
from data.generated_enums import ItemCategoryHashes
from data.bounties.bounty_config import (
    KillType,
    matchTable,
    assignModel,
    matchTableModel,
)

Result = dict
BountyMetadata = assignModel
AssignmentCategory = list(matchTable[0].assign.dict().keys())

logger.info("Generating Bounty data...")
loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")

# debug = False
# debugRecords = False

# # 要处理的 Item 类型
# categoryAllowList = [ItemCategoryHashes.任务步骤, ItemCategoryHashes.悬赏]

# # collects bounty->definition associations
# bounties: dict[str, BountyMetadata] = {}


# def assign(ruleset: matchTableModel, bounty: BountyMetadata) -> None:
#     for assignTo, assignValues in ruleset.get("assign", {}).items():
#         if assignTo in AssignmentCategory:
#             target = getattr(bounty, assignTo)
#             target1 = target or []
#             target2 = assignValues or []
#             target = [*target1, *target2]


# def getObjInfo(item: dict) -> str:
#     if objectives := item.get("objectives"):
#         ret = ""
#         for o in objectives["objectiveHashes"]:
#             obj = get("DestinyObjectiveDefinition", o)
#             string = obj.get("displayProperties", {"name": None})["name"] or obj.get(
#                 "progressDescription"
#             )
#             ret += str(string)
#         return ret
#     return ""


# accessors = {
#     "name": lambda item: item["displayProperties"]["name"],
#     "desc": lambda item: item["displayProperties"]["description"],
#     "obj": getObjInfo,
#     "type": lambda item: item["itemTypeAndTierDisplayName"],
#     "label": lambda item: item.get("inventory", {"stackUniqueLabel": None}).get(
#         "stackUniqueLabel"
#     ),
# }

# matchTypes = ["name", "desc", "obj", "type", "label"]

# for inventoryItem in inventoryItems:
#     if (
#         not [
#             i
#             for i in categoryAllowList
#             if i in inventoryItem.get("itemCategoryHashes", [])
#         ]
#     ) and not (
#         (inventory := inventoryItem.get("inventory"))
#         and (stackUniqueLabel := inventory.get("stackUniqueLabel"))
#         and "bounties" in stackUniqueLabel
#     ):
#         continue

#     thisBounty = BountyMetadata.parse_obj({})
#     for ruleset in matchTable:
#         for matchType in matchTypes:
#             if matchs := getattr(ruleset, matchType):
#                 for match in matchs:
#                     match = re.compile(match, flags=re.I)
#                     stringToTest = accessors[matchType](inventoryItem)
#                     if stringToTest and re.search(match, stringToTest):
#                         assign(ruleset, thisBounty)

# 麻了 这个悬赏我搞不来，回头直接copy人家输出的json吧


def flattenRecords(hash: int) -> List[int]:
    node = get("DestinyPresentationNodeDefinition", hash)
    if node:
        records = [i.get("recordHash") for i in node["children"]["records"]] or []
        if presentationNodes := node["children"]["presentationNodes"]:
            for i in presentationNodes:
                records.extend(flattenRecords(i["presentationNodeHash"]))
    else:
        records = []
    return records


recordHashes = flattenRecords(3443694067)
recordInfo = dict
# 这个赛季挑战也是，后面再说
logger.warning("这个脚本还没写完")
logger.info("Generating Bounty data... Done")
