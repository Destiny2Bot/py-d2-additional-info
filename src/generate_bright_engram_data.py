from typing import List

import ujson

from log import logger
from tools import readFile, writeFile, sortObject
from manifest import get, getAll, loadLocal
from data.generated_enums import ItemCategoryHashes
from data.seasons.d2_season_info import D2CalculatedSeason

seasons = ujson.loads(readFile("./data/seasons/seasons_unfiltered.json"))

logger.info("Generating Bright Engram data...各赛季光明记忆水晶")

loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")

loadLocal(language="en")
inventoryItems_en = getAll("DestinyInventoryItemDefinition", language="en")

brightEngramExclusions = [
    "血色",
    "狂欢",
    "曙光",
    "英灵日",
    "至日",
]

brightEngrams: dict[int, int] = {}


def hasTerm(string: str, terms: List[str]):
    return any([i for i in terms if i in string])


for inventoryItem in inventoryItems:
    hash, itemTypeDisplayName = (
        inventoryItem["hash"],
        inventoryItem.get("itemTypeDisplayName"),
    )
    description, name = (
        inventoryItem["displayProperties"]["description"],
        inventoryItem["displayProperties"]["name"],
    )
    categoryHashes = inventoryItem.get("itemCategoryHashes") or []
    if (
        # 属于记忆水晶分类
        ItemCategoryHashes.记忆水晶 in categoryHashes
        # 类型是光明记忆水晶
        and "光明记忆水晶" in itemTypeDisplayName
        # 不是活动奖励
        and not hasTerm(description, brightEngramExclusions)
        # 不是活动奖励
        and not hasTerm(name, brightEngramExclusions)
        # 并且这个哈希有一个相应的供应商表
        and get("DestinyVendorDefinition", hash)
    ):
        # 获取这个道具的赛季信息
        if season := seasons.get(str(hash)):
            brightEngrams[season] = hash
            logger.debug(f"{season}\t{hash}\t{name}")

for season in range(1, D2CalculatedSeason + 1):
    if not brightEngrams.get(season):
        brightEngrams[season] = brightEngrams[season - 1]
        logger.debug(f"{season}\t{brightEngrams[season]}")

# 各赛季的光明记忆水晶(不包含活动奖励)
brightEngrams = sortObject(brightEngrams)
writeFile("./output/bright-engrams.json", brightEngrams)
logger.success("writeFile ./output/bright-engrams.json")
logger.info("Generating Bright Engram data...Done")
