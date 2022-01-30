from typing import Dict, List, Union

from pydantic import BaseModel

from tools import writeFile
from manifest import getAll, loadLocal
from data.generated_enums import ItemCategoryHashes

loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")


class Telemetry(BaseModel):
    arc: bool
    void: bool
    solar: bool


class GhostType(BaseModel):
    xp: bool
    resource: bool
    caache: bool
    scanner: bool
    glimmer: bool
    telemetry: Telemetry
    improved: bool


class GhostData(BaseModel):
    location: Union[str, bool]
    type: GhostType


ghostPerks: Dict[str, GhostData] = {}

# 随机模组
ghostPerkHashDenyList = [2328497849]

for item in inventoryItems:
    hash: int = item["hash"]
    description: str = item["displayProperties"]["displayProperties"]
    categoryHashes: List[int] = item["itemCategoryHashes"] or []

    if (ItemCategoryHashes.机灵模组特性 in categoryHashes) and (
        hash not in ghostPerkHashDenyList
    ):
        # WIP
        pass

writeFile("./output/ghost-perks.json", ghostPerks)
