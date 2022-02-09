from typing import List

from tools import writeFile, dedupeAndSortArray
from manifest import getAll, loadLocal

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
