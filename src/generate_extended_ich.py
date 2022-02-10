from log import logger
from tools import writeFile, sortObject
from manifest import getAll, loadLocal
from data.generated_enums import ItemCategoryHashes

logger.info("Generating Extended ICH... 所有榴弹发射器和精密框架霰弹枪的物品 hash")
loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")

ffGrenadeLaunchers = [
    item
    for item in inventoryItems
    if (itemCategoryHashes := item.get("itemCategoryHashes"))
    and ItemCategoryHashes.榴弹发射器 in itemCategoryHashes
    and ItemCategoryHashes.威能武器 not in itemCategoryHashes
    and ItemCategoryHashes.样品模型 not in itemCategoryHashes
]

slugShotguns = [
    item
    for item in inventoryItems
    if (itemCategoryHashes := item.get("itemCategoryHashes"))
    and ItemCategoryHashes.霰弹枪 in itemCategoryHashes
    and ItemCategoryHashes.样品模型 not in itemCategoryHashes
    and (sockets := item.get("sockets"))
    and sockets["socketEntries"][0].get("singleInitialItemHash") == 918679156  # 精密框架
]

extendedICH: dict[int, int] = {}

for gl in ffGrenadeLaunchers:
    extendedICH[gl["hash"]] = -ItemCategoryHashes.榴弹发射器

for ssg in slugShotguns:
    extendedICH[ssg["hash"]] = -ItemCategoryHashes.霰弹枪

extendedICH = sortObject(extendedICH)

# 所有榴弹发射器和精密框架霰弹枪的物品 hash
writeFile("./output/extended-ich.json", extendedICH)
logger.success("writeFile ./output/extended-ich.json")
logger.info("Generating Extended ICH... Done")
