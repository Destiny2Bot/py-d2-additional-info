import re
from typing import List

from log import logger
from tools import writeFile, sortObject, dedupeAndSortArray
from manifest import get, getAll, loadLocal
from data.generated_enums import ItemCategoryHashes
from data.bounties.bounty_config import (
    KillType,
    BountyMetadata,
    matchTable,
    matchTableModel,
)

Result = dict
AssignmentCategory = list(matchTable[0].assign.dict().keys())

logger.info("Generating Bounty data... 悬赏单及赛季任务信息")
loadLocal(language="en")
# loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition", language="en")
# inventoryItems_zh = getAll("DestinyInventoryItemDefinition")


# 要处理的 Item 类型
categoryAllowList = [ItemCategoryHashes.任务步骤, ItemCategoryHashes.悬赏]

# collects bounty->definition associations
bounties: dict[str, dict] = {}


def assign(ruleset: matchTableModel, bounty: BountyMetadata) -> None:
    for assignTo, assignValues in ruleset.dict(exclude_none=True)["assign"].items():
        target = getattr(bounty, assignTo) or []
        target.extend(assignValues)
        target = dedupeAndSortArray(target)
        setattr(bounty, assignTo, target)


def getObjInfo(item: dict) -> str:
    if objectives := item.get("objectives"):
        ret = ""
        for o in objectives["objectiveHashes"]:
            obj = get("DestinyObjectiveDefinition", o, language="en")
            string = obj.get("displayProperties", {"name": None})["name"] or obj.get(
                "progressDescription"
            )
            ret += str(string)
        return ret
    return ""


accessors = {
    "name": lambda item: item["displayProperties"]["name"],
    "desc": lambda item: item["displayProperties"]["description"],
    "obj": getObjInfo,
    "type": lambda item: item["itemTypeAndTierDisplayName"],
    "label": lambda item: item.get("inventory", {"stackUniqueLabel": None}).get(
        "stackUniqueLabel"
    ),
}


def getRecordObjInfo(item: dict) -> str:
    if objectiveHashes := item.get("objectiveHashes"):
        ret = ""
        for o in objectiveHashes:
            obj = get("DestinyObjectiveDefinition", o, language="en")
            string = obj.get("displayProperties", {"name": None})["name"] or obj.get(
                "progressDescription"
            )
            ret += str(string)
        return ret
    return ""


recordAccessors = {
    "name": lambda item: item["displayProperties"]["name"],
    "desc": lambda item: item["displayProperties"]["description"],
    "obj": getRecordObjInfo,
    "type": lambda item: None,
    "label": lambda item: None,
}

matchTypes = ["name", "desc", "obj", "type", "label"]

for inventoryItem in inventoryItems:
    if (
        not [
            i
            for i in categoryAllowList
            if i in inventoryItem.get("itemCategoryHashes", [])
        ]
    ) and not (
        (inventory := inventoryItem.get("inventory"))
        and (stackUniqueLabel := inventory.get("stackUniqueLabel"))
        and "bounties" in stackUniqueLabel
    ):
        continue

    thisBounty = BountyMetadata.parse_obj({})
    for ruleset in matchTable:
        for matchType in matchTypes:
            if matchs := getattr(ruleset, matchType):
                for match in matchs:
                    stringToTest = accessors[matchType](inventoryItem)
                    if match.endswith("#i"):
                        match = re.compile(match[:-2], flags=re.I)
                    else:
                        match = re.compile(match)
                    if stringToTest and re.search(match, stringToTest):
                        assign(ruleset, thisBounty)
    if thisBounty.dict(exclude_none=True):
        bounties[inventoryItem["hash"]] = {
            k: v for k, v in thisBounty.dict().items() if v
        }
bounties = sortObject(bounties)
# 悬赏任务信息
writeFile("./output/pursuits.json", bounties)
logger.success("writeFile ./output/pursuits.json")


def flattenRecords(hash: int) -> List[int]:
    node = get("DestinyPresentationNodeDefinition", hash, language="en")
    if node:
        records = [i.get("recordHash") for i in node["children"]["records"]] or []
        if presentationNodes := node["children"]["presentationNodes"]:
            for i in presentationNodes:
                records.extend(flattenRecords(i["presentationNodeHash"]))
    else:
        records = []
    return records


recordHashes = flattenRecords(3443694067)
recordInfo: dict = {}
for recordHash in recordHashes:
    record = get("DestinyRecordDefinition", recordHash, language="en")
    if not record:
        continue

    thisBounty = BountyMetadata.parse_obj({})
    for ruleset in matchTable:
        for matchType in matchTypes:
            if matchs := getattr(ruleset, matchType):
                for match in matchs:
                    stringToTest = recordAccessors[matchType](record)
                    if match.endswith("#i"):
                        match = re.compile(match[:-2], flags=re.I)
                    else:
                        match = re.compile(match)
                    if stringToTest and re.search(match, stringToTest):
                        assign(ruleset, thisBounty)
    if thisBounty.dict(exclude_none=True):
        recordInfo[record["hash"]] = {k: v for k, v in thisBounty.dict().items() if v}

recordInfo = sortObject(recordInfo)
# 赛季挑战任务信息
writeFile("./output/seasonal-challenges.json", recordInfo)
logger.success("writeFile ./output/seasonal-challenges.json")
logger.info("Generating Bounty data... Done")
