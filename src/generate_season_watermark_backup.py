import ujson

from log import logger
from tools import readFile, writeFile, sortObject
from manifest import getAll, loadLocal

seasons = ujson.loads(readFile("./data/seasons/seasons_unfiltered.json"))
watermarkToSeason: dict[str, int] = ujson.loads(
    readFile("./output/watermark-to-season.json")
)

logger.info("Generating Season Watermark Backup...输出非赛季与活动水印")
loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")
backupData: dict[str, int] = {}

for inventoryItem in inventoryItems:
    hash = inventoryItem["hash"]
    watermark = inventoryItem.get("iconWatermark")
    shelved = inventoryItem.get("iconWatermarkShelved")
    ich = inventoryItem.get("itemCategoryHashes") or []
    test = watermarkToSeason.get(watermark) or watermarkToSeason.get(shelved)
    if (not test) and watermark and 59 not in ich:
        backupData[hash] = seasons[str(hash)]

backupData = sortObject(backupData)

# 输出非赛季与活动水印
writeFile("./output/seasons_backup.json", backupData)
logger.success("writeFile ./output/seasons_backup.json")
logger.info("Generating Season Watermark Backup...Done")
