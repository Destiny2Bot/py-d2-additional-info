from typing import Final

from log import logger
from tools import writeFile
from manifest import get, getAll, loadLocal

logger.info("Generating catalyst data...")
loadLocal()

catalystPresentationNodeHash: Final[int] = 1984921914

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
