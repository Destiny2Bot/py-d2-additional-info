from typing import List

from log import logger
from tools import writeFile, dedupeAndSortArray
from manifest import getAll, loadLocal

logger.info("Generating Raid Mods... raid 模组类型标识")
loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")
lastWishRaidModPlugCategoryIdentifier = "enhancements.season_outlaw"
raidModPlugCategoryIdentifier = "enhancements.raid_"


def findAllRaidPlugCategoryHashes() -> List:
    raidModPlugCategoryHashes = []
    for inventoryItem in inventoryItems:
        if plug := inventoryItem.get("plug"):
            if (
                plug["plugCategoryIdentifier"].startswith(raidModPlugCategoryIdentifier)
                or plug["plugCategoryIdentifier"]
                == lastWishRaidModPlugCategoryIdentifier
            ):
                raidModPlugCategoryHashes.append(plug["plugCategoryHash"])
    return raidModPlugCategoryHashes


raidModPlugCategoryHashes = findAllRaidPlugCategoryHashes()

raidModPlugCategoryHashes = dedupeAndSortArray(raidModPlugCategoryHashes)

# 输出 raid 模组类型标识
writeFile("./output/raid-mod-plug-category-hashes.json", raidModPlugCategoryHashes)
logger.success("writeFile ./output/raid-mod-plug-category-hashes.json")
logger.info("Generating Raid Mods... Done")
