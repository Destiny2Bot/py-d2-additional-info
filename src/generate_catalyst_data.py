from typing import Union

from log import logger
from tools import writeFile
from manifest import get, getAll, loadLocal

logger.info("Generating catalyst data...")
loadLocal()


def getCatalystPresentationNodeHash() -> Union[int, None]:
    presentationNodes = getAll("DestinyPresentationNodeDefinition")
    catNode = [
        p
        for p in presentationNodes
        if p["displayProperties"]["name"] == "异域催化"
        and len(p["children"]["presentationNodes"]) > 1
    ]
    if catNode:
        return catNode[0]["hash"]
    else:
        return None


catalystPresentationNodeHash = getCatalystPresentationNodeHash()

inventoryItems = getAll("DestinyInventoryItemDefinition")

triumphData: dict[int, str] = {}

if (
    presentationNodeDefinition := get(
        "DestinyPresentationNodeDefinition", catalystPresentationNodeHash
    )
) is None:
    raise Exception("catalystPresentationNode not found")
for presentationNode in presentationNodeDefinition["children"]["presentationNodes"]:
    if (
        _presentNodeDefinition := (
            get(
                "DestinyPresentationNodeDefinition",
                presentationNode["presentationNodeHash"],
            )
        )
    ) is None:
        continue
    for record in _presentNodeDefinition["children"]["records"]:
        if (r := get("DestinyRecordDefinition", record["recordHash"])) is None:
            continue
        recordName = r["displayProperties"]["name"]
        itemWithSameName = None
        for item in inventoryItems:
            if (
                item["displayProperties"]["name"] == recordName
                and item["inventory"]["tierType"] == 6
            ):
                itemWithSameName = item
                break
        if itemWithSameName is None:
            continue
        icon = itemWithSameName.get("displayProperties")
        if icon is None:
            continue
        icon = icon["icon"]
        triumphData[record["recordHash"]] = icon
        logger.debug(f"{recordName} -> {icon}")

writeFile(
    "./output/catalyst-triumph-icons.json",
    {x: triumphData[x] for x in sorted(triumphData)},
)
# 催化剂
logger.success("writeFile ./output/catalyst-triumph-icons.json")
logger.info("Generating catalyst data... Done")
