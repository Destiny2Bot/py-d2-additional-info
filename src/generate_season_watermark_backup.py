import ujson

from tools import readFile, writeFile, sortObject
from manifest import getAll, loadLocal

seasons = ujson.loads(readFile("./data/seasons/seasons_unfiltered.json"))
watermarkToSeason: dict[str, int] = ujson.loads(
    readFile("./output/watermark-to-season.json")
)


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

# 输出 watermark-to-season.json 未记录的水印
writeFile("./output/seasons_backup.json", backupData)
