from typing import List

from bungieapi.generated.components.schemas.destiny import DestinyItemType

from tools import writeFile, dedupeAndSortArray
from manifest import get, getAll, loadLocal

loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")

trialsObjectives: dict[int, str] = {}
trialsPassages: List[int] = []

for inventoryItem in inventoryItems:
    if (
        inventoryItem.get("itemTypeDisplayName") == "试炼入场券"
        and inventoryItem["displayProperties"]["name"].endswith("入场券")
        and inventoryItem.get("itemType") != DestinyItemType.DUMMY.value
    ):
        trialsPassages.append(inventoryItem["hash"])
        if objectives := inventoryItem.get("objectives"):
            for o in objectives.get("objectiveHashes"):
                if obj := get("DestinyObjectiveDefinition", o):
                    if obj["progressDescription"] == "无瑕":
                        if obj.get("completedValueStyle") == 10:
                            trialsObjectives[obj["hash"]] = obj.get(
                                "displayProperties", {}
                            ).get("name") or obj.get("progressDescription", "")
                    else:
                        trialsObjectives[obj["hash"]] = obj.get(
                            "displayProperties", {}
                        ).get("name") or obj.get("progressDescription", "")

trialsMetadata = {
    "passages": dedupeAndSortArray(trialsPassages),
    "objectives": trialsObjectives,
}

# 输出奥西里斯试炼门票信息
writeFile("./output/d2-trials-objectives.json", trialsMetadata)
