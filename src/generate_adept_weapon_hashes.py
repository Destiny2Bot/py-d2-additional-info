from typing import Union

from bungieapi.generated.components.schemas.destiny import DestinyItemType

from tools import writeFile
from manifest import getAll, loadLocal

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

writeFile("./output/adept-weapon-hashes.json", adeptWeaponHashes)
