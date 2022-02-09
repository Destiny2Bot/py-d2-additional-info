from typing import List

import ujson

from log import logger
from tools import annotate, writeFile, sortObject, dedupeAndSortArray
from manifest import getAll, loadLocal
from src.generate_source_info import Categories, applySourceStringRules

categories = Categories.parse_file("./data/sources/categories.json")

loadLocal(language="en")

inventoryItems = getAll("DestinyInventoryItemDefinition", language="en")
collectibles = getAll("DestinyCollectibleDefinition", language="en")
hashToMissingCollectibleHash: dict[str, int] = {}

# 没有可收集哈希的库存物品
nonCollectibleItems = [
    item for item in inventoryItems if not item.get("collectibleHash")
]

# 有可收集哈希的库存物品
collectibleItems = [item for item in inventoryItems if item.get("collectibleHash")]


def stringifySortCompare(arr1: List[int], arr2: List[int]):
    return sorted(arr1) == sorted(arr2)


for collectibleItem in collectibleItems:
    itemsWithSameName = [
        nonCollectibleItem
        for nonCollectibleItem in nonCollectibleItems
        if collectibleItem["displayProperties"].get("name")
        and collectibleItem["displayProperties"]["name"]
        == nonCollectibleItem["displayProperties"]["name"]
        and stringifySortCompare(
            collectibleItem.get("itemCategoryHashes", []),
            nonCollectibleItem.get("itemCategoryHashes", []),
        )
    ]

    for nonCollectibleItem in itemsWithSameName:
        collectibleinfo = [
            sourceHash
            for collectible in collectibles
            if collectibleItem["collectibleHash"] == collectible["hash"]
            and (sourceHash := collectible.get("sourceHash"))
        ][0]
        hashToMissingCollectibleHash[nonCollectibleItem["hash"]] = collectibleinfo

hashToMissingCollectibleHash = sortObject(hashToMissingCollectibleHash)
sourcesInfo: dict[int, str] = {}
D2Sources: dict[str, List[int]] = {}
newSourceInfo: dict[str, List[int]] = {}

for collectible in collectibles:
    if collectible.get("sourceHash"):
        sourcesInfo[collectible["sourceHash"]] = collectible.get("sourceString")


# 循环进行分类
for sourceTag, matchRule in categories.sources.items():
    if sourceTag == "ignore":
        continue
    D2Sources[sourceTag] = applySourceStringRules(sourcesInfo, matchRule)

    if not len(D2Sources[sourceTag]):
        logger.warning(f"no matching sources for {sourceTag}: {matchRule.dict()}")

    sourceHashes = D2Sources[sourceTag]
    newSourceInfo[sourceTag] = newSourceInfo.get(sourceTag) or []
    for hash, sourceHash in hashToMissingCollectibleHash.items():
        if sourceHash in sourceHashes:
            newSourceInfo[sourceTag].append(int(hash))

    newSourceInfo[sourceTag] = dedupeAndSortArray(newSourceInfo[sourceTag])

    if alias := matchRule.alias:
        newSourceInfo[alias] = newSourceInfo[sourceTag]

D2SourcesSorted = sortObject(newSourceInfo)

pretty = f"""missingSources = {ujson.dumps(D2SourcesSorted, ensure_ascii=False, indent=4)}
"""
annotated = annotate(pretty, sourcesInfo)

# 没有可收集哈希的库存物品进行分类
writeFile("./output/missing_source_info.py", annotated)
