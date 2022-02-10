from typing import List

import ujson

from log import logger
from tools import readFile, writeFile, diffArrays, dedupeAndSortArray
from manifest import getAll, loadLocal
from data.generated_enums import ItemCategoryHashes

allWatermarks = ujson.loads(readFile("./data/seasons/all-watermarks.json"))
seasons = ujson.loads(readFile("./data/seasons/seasons_unfiltered.json"))
watermarkToSeason: dict[str, int] = ujson.loads(
    readFile("./output/watermark-to-season.json")
)

logger.info("Generating watermark info... 赛季及活动水印图标")
loadLocal()


inventoryItems = getAll("DestinyInventoryItemDefinition")

itemsNoMods = [
    item
    for item in inventoryItems
    if (not item.get("itemCategoryHashes"))
    or (ItemCategoryHashes.模组_MOD not in item.get("itemCategoryHashes"))
]
watermarks: List[str] = []
for item in itemsNoMods:
    if quality := item.get("quality"):
        watermarks.extend(
            [i for i in item["quality"]["displayVersionWatermarkIcons"] if i]
        )

        if iconWatermark := item.get("iconWatermark"):
            watermarks.append(iconWatermark)
            # item["quality"]["displayVersionWatermarkIcons"].extend(item["iconWatermark"])

watermarks.extend(
    [
        iconWatermarkShelved
        for item in itemsNoMods
        if (iconWatermarkShelved := item.get("iconWatermarkShelved"))
    ]
)

watermarks = dedupeAndSortArray(watermarks)

newWatermarks = diffArrays(watermarks, allWatermarks)

if len(newWatermarks):
    for newWatermark in newWatermarks:
        item = [
            item
            for item in inventoryItems
            if item.get("iconWatermark") == newWatermark
            or item.get("iconWatermarkShelved") == newWatermark
        ]
        if item:
            item = item[0]
        else:
            continue
        watermark = (
            iconWatermark
            if (iconWatermark := item.get("iconWatermark"))
            else item.get("iconWatermarkShelved")
        )
        watermarkToSeason[watermark] = seasons[str(item["hash"])]
        logger.info(f"New watermark: {watermark}\t{seasons[str(item['hash'])]}")
    # 输出所有水印图标 URL
    writeFile("./data/seasons/all-watermarks.json", watermarks)

watermarkHashesEvents: dict[int, int] = {
    269339124: 1,  # Dawning Hope (Dawning) 曙光节
    1052553863: 2,  # Crimson Passion (Crimson Days) 血色浪漫日
    3859483819: 3,  # Malachite Gold (Solstice of Heroes) 至日英雄
    2233576420: 4,  # Fright Night (Festival of the Lost) 英灵日
    1914989540: 5,  # Verdant Crown (Revelry) 狂欢节
    2171727442: 6,  # Rivalry Blacksand (Guardian Games) 守护者游戏
}

watermarkToEvent: dict[str, int] = {}

for hash in watermarkHashesEvents.keys():
    item = [item for item in inventoryItems if item["hash"] == hash]
    if item:
        item = item[0]
    else:
        continue
    if iconWatermark := item.get("iconWatermark"):
        watermarkToEvent[iconWatermark] = watermarkHashesEvents[hash]

# 输出所有赛季水印图标 URL
writeFile("./output/watermark-to-season.json", watermarkToSeason)
logger.success("writeFile ./output/watermark-to-season.json")
# # 输出所有活动水印图标 URL
writeFile("./output/watermark-to-event.json", watermarkToEvent)
logger.success("writeFile ./output/watermark-to-event.json")

logger.info("Generating watermark info... Done")
