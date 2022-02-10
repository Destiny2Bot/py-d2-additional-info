from typing import Optional

from log import logger
from tools import writeFile
from manifest import getAll, loadLocal

logger.info("Generating Workaround items... ")
loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")
collectibles = getAll("DestinyCollectibleDefinition")


itemReplacementTable: dict[int, int] = {}


def get_badItem(inventoryItems, item) -> Optional[dict]:
    for correspondingItem in inventoryItems:
        if (
            correspondingItem["hash"] != item["hash"]
            and correspondingItem["displayProperties"]["name"]
            == item["displayProperties"]["name"]
            and correspondingItem["inventory"]["bucketTypeHash"] == 2422292810
        ):
            return correspondingItem
    return None


def collectibles_test(collectibleHash: int) -> bool:
    for collectable in collectibles:
        if collectable["hash"] == collectibleHash and (
            collectable["sourceHash"] == 1618754228
            or collectable["sourceHash"] == 2627087475
        ):
            return True
    return False


for item in inventoryItems:
    if (
        (1 in item.get("itemCategoryHashes", [-1]))
        and item.get("collectibleHash")
        and (collectibles_test(item["collectibleHash"]))
    ):
        badItem = get_badItem(inventoryItems, item)
        if badItem:
            itemReplacementTable[badItem["hash"]] = item["hash"]
            logger.debug(
                f"{badItem['displayProperties']['name']}[{badItem['hash']}] -> {item['displayProperties']['name']}[{item['hash']}]"
            )

writeFile("./output/item-def-workaround-replacements.json", itemReplacementTable)
logger.success("writeFile ./output/item-def-workaround-replacements.json")
logger.info("Generating Workaround items... Done")
