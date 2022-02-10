from typing import Union

from bungieapi.generated.components.schemas.destiny import DestinyItemType

from log import logger
from tools import writeFile
from manifest import getAll, loadLocal

logger.info("Generating Adept Weapon Hashes... 所有专家和失间武器的物品 hash")
loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")
adeptWeaponHashes: Union[list, filter] = filter(
    lambda x: (
        str(x["displayProperties"]["name"]).strip().endswith("（专家）")
        or str(x["displayProperties"]["name"]).strip().endswith("（失时）")
        and x["itemType"] == DestinyItemType.WEAPON
    ),
    inventoryItems,
)


adeptWeaponHashes = [x["hash"] for x in adeptWeaponHashes]

# 所有专家和失间武器的物品 hash
writeFile("./output/adept-weapon-hashes.json", adeptWeaponHashes)
logger.success("writeFile ./output/adept-weapon-hashes.json")
logger.info("Generating Adept Weapon Hashes... Done")
