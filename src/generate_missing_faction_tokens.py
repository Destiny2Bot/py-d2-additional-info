from typing import List

from log import logger
from tools import writeFile, dedupeAndSortArray
from manifest import getAll, loadLocal

logger.info("Generating missing faction tokens... 没有指定库存物品的派系与相关NPC信息")
loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")
factions = getAll("DestinyFactionDefinition")

allTokenHashes: List = []
for i in [
    list(tokenValues.keys())
    for faction in factions
    if (tokenValues := faction.get("tokenValues"))
]:
    allTokenHashes.extend(i)
allTokenHashes = [int(i) for i in allTokenHashes]
allTokenHashes = dedupeAndSortArray(allTokenHashes)

missingTokenHashes: List[int] = []
badVendors: List[int] = []
for hash in allTokenHashes:
    item = [item for item in inventoryItems if item["hash"] == hash]
    if not item:
        missingTokenHashes.append(hash)
        vendor = [i for i in factions if hash in i.get("tokenValues", {}).keys()]
        if vendor:
            badVendors.append(vendor[0]["hash"])

# 输出没有指定库存物品的派系 tokenValues
writeFile("./output/missing-faction-tokens.json", missingTokenHashes)
logger.success("writeFile ./output/missing-faction-tokens.json")
# 输出没有指定库存物品的派系 tokenValues 的NPC hash
writeFile("./output/bad-vendors.json", badVendors)
logger.success("writeFile ./output/bad-vendors.json")

logger.info("Generating missing faction tokens... Done")
