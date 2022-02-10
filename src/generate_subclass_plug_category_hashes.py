from typing import List

from log import logger
from tools import writeFile, dedupeAndSortArray
from manifest import get, getAll, loadLocal

logger.info("Generating Subclass Plug Category Hashes... 职业技能插槽类型")
loadLocal()


def getItem(hash: int) -> dict:
    return get("DestinyInventoryItemDefinition", hash)


def getPlugSet(hash: int) -> dict:
    return get("DestinyPlugSetDefinition", hash)


allItems = getAll("DestinyInventoryItemDefinition")

classBucketHash = 3284755031

# 插槽类型 hash
abilitiesSocketCategoryHash = 309722977
aspectsSocketCategoryHash = 2140934067
fragmentsSocketCategoryHash = 1313488945

# 当前未使用，但如果我们有超级选择(super choices)，这将是必需的
superSocketCategoryHash = 457473665

wantedCategoryHashes = [
    abilitiesSocketCategoryHash,
    aspectsSocketCategoryHash,
    fragmentsSocketCategoryHash,
    superSocketCategoryHash,
]


def findAllSubclassPlugs():
    plugTracker: dict[str, int] = {}
    for item in allItems:
        if (
            (inventory := item.get("inventory"))
            and inventory.get("bucketTypeHash") == classBucketHash
            and item.get("sockets")
        ):
            indexes: List[int] = []

            # 获取所有具有正确类别哈希的插槽索引(socket indexes)
            for socketCategory in item["sockets"].get("socketCategories"):
                if socketCategory.get("socketCategoryHash") in wantedCategoryHashes:
                    for index in socketCategory["socketIndexes"]:
                        indexes.append(index)
            for socketIndex in indexes:
                socket = item.get("sockets", {}).get("socketEntries", [])[socketIndex]
                plugSet = (
                    getPlugSet(reusablePlugSetHash)
                    if (reusablePlugSetHash := socket.get("reusablePlugSetHash"))
                    else {}
                )
                plugItems = (
                    [
                        getItem(reusablePlugItem["plugItemHash"])
                        for reusablePlugItem in reusablePlugItems
                    ]
                    if (reusablePlugItems := plugSet.get("reusablePlugItems"))
                    else []
                )
                for plugItem in plugItems:
                    if plugCategoryHash := plugItem.get("plug", {}).get(
                        "plugCategoryHash"
                    ):
                        plugTracker[
                            plugItem["displayProperties"]["name"]
                        ] = plugCategoryHash
    return dedupeAndSortArray(list(plugTracker.values()))


subclassPlugs = findAllSubclassPlugs()

# 输出职业技能插槽类型 hash
writeFile("./output/subclass-plug-category-hashes.json", subclassPlugs)
logger.success("writeFile ./output/subclass-plug-category-hashes.json")
logger.info("Generating Subclass Plug Category Hashes... Done")
