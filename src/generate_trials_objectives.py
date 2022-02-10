from typing import List

from log import logger
from tools import writeFile, dedupeAndSortArray
from manifest import get, getAll, loadLocal

logger.info("Generating Trials Objectives...")
loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")

trialsObjectives: dict[int, str] = {}
trialsPassages: List[int] = []

for inventoryItem in inventoryItems:
    if (
        inventoryItem.get("itemTypeDisplayName") == "试炼入场券"
        and inventoryItem["displayProperties"]["name"].endswith("入场券")
        and inventoryItem.get("itemType") != 20
    ):
        trialsPassages.append(inventoryItem["hash"])
        logger.debug(
            f"Found Trials Passage: {inventoryItem['displayProperties']['name']}\t{inventoryItem['hash']}"
        )
        if objectives := inventoryItem.get("objectives"):
            for o in objectives.get("objectiveHashes"):
                if obj := get("DestinyObjectiveDefinition", o):
                    if obj["progressDescription"] == "无瑕":
                        if obj.get("completedValueStyle") == 10:
                            trialsObjectives[obj["hash"]] = obj.get(
                                "displayProperties", {}
                            ).get("name") or obj.get("progressDescription", "")
                            logger.debug(
                                f"Found Trials Objective: {trialsObjectives[obj['hash']]}\t{obj['hash']}"
                            )
                    else:
                        trialsObjectives[obj["hash"]] = obj.get(
                            "displayProperties", {}
                        ).get("name") or obj.get("progressDescription", "")
                        logger.debug(
                            f"Found Trials Objective: {trialsObjectives[obj['hash']]}\t{obj['hash']}"
                        )

trialsMetadata = {
    "passages": dedupeAndSortArray(trialsPassages),
    "objectives": trialsObjectives,
}

# 输出奥西里斯试炼门票信息
writeFile("./output/d2-trials-objectives.json", trialsMetadata)
logger.success("wirteFile: ./output/d2-trials-objectives.json")
