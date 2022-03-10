from log import logger
from tools import writeFile
from manifest import getAll, loadLocal

loadLocal()
logger.info("Generating Craftable Hashes... 所有可制作武器")

inventoryItems = getAll("DestinyInventoryItemDefinition")

craftableHashes = [
    i["crafting"]["outputItemHash"] for i in inventoryItems if i.get("crafting")
]

writeFile("./output/craftable-hashes.json", craftableHashes)
logger.success("wirteFile: ./output/craftable-hashes.json")
