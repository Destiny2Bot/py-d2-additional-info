# 为可制造武器收集增强的内在特性，以便我们可以正确处理它们的奖励统计数据。

import re
from typing import List

from log import logger
from tools import writeFile
from manifest import getAll, loadLocal
from data.generated_enums import PlugCategoryHashes

# from .flipped_enums import DestinyItemType

loadLocal()

logger.info("Generating Crafting Resonant Elements... 深视武器提示信息")
allResonantElements: List[dict] = []

objectives = getAll("DestinyObjectiveDefinition")
inventoryItems = getAll("DestinyInventoryItemDefinition")

resonanceExtractionPlugs = [
    i
    for i in inventoryItems
    if (plug := i.get("plug"))
    and plug["plugCategoryHash"] == PlugCategoryHashes.CraftingPlugsWeaponsModsExtractors
    and i["displayProperties"]["name"]
]

for plug in resonanceExtractionPlugs:
    materialName: str = plug["displayProperties"]["name"]
    objectiveDef = [
        o for o in objectives if o.get("progressDescription") == materialName
    ]
    if objectiveDef:
        tag = materialName.lower().replace(" ", "").replace("元素", "")
        if tag:
            allResonantElements.append(
                {
                    "objectiveHash": objectiveDef[0]["hash"],
                    "tag": tag,
                    "name": materialName,
                }
            )
            logger.debug(
                f"'{materialName}' -> '{tag}' (hash: {objectiveDef[0]['hash']})"
            )
        else:
            logger.debug(f"Unable to map '{materialName}' to tag.")
    else:
        logger.debug(f"No objective found for '{materialName}'")

capacityMatcher = r"你已经达到或接近.+元素的最大容量！\n\n容量：\{var:(\d+)\}\/\{var:(\d+)\}"

craftingMaterialCounts: dict = {}

for item in resonanceExtractionPlugs:
    if tooltipNotifications := item.get("tooltipNotifications"):
        if match := re.match(capacityMatcher, tooltipNotifications[0]["displayString"]):
            currentCountHash, maxCapacityHash = match.groups()
            craftingMaterialCounts[item["displayProperties"]["name"]] = {
                "label": item["displayProperties"]["name"],
                "currentCountHash": int(currentCountHash),
                "maxCapacityHash": int(maxCapacityHash),
                "plugHash": item["hash"],
            }


def getMatchingDummyItem(label):
    matchingDummyItem = [
        i
        for i in inventoryItems
        if i.get("itemType") == 20 and i["displayProperties"]["name"] == label
    ]
    if matchingDummyItem:
        return matchingDummyItem[0]["hash"]
    else:
        return 0


prettyResonantElements = "\n".join(
    [f'  {e["objectiveHash"]}: "{e["tag"]}", # {e["name"]}' for e in allResonantElements]
)

prettyCraftingMaterialCounts = "\n".join(
    [
        f"  {{'currentCountHash': {i['currentCountHash']}, 'maxCapacityHash': {i['maxCapacityHash']}, 'materialHash': {getMatchingDummyItem(i['label']) or i['plugHash']}}}, # {i['label']}"
        for i in craftingMaterialCounts.values()
    ]
)
outString = f"""
resonantElementTagsByObjectiveHash: dict = {{
{prettyResonantElements}
}}

resonantMaterialStringVarHashes = [
{prettyCraftingMaterialCounts}
]
"""

writeFile("./output/crafting_resonant_elements.py", outString)
logger.success("writeFile ./output/crafting_resonant_elements.py")
