from log import logger
from tools import writeFile
from manifest import get, getAll, loadLocal
from data.generated_enums import ItemCategoryHashes

logger.info("Generating Engram Rarity icons... 光球图标")
loadLocal()

results: dict[str, str] = {}
for i in getAll("DestinyInventoryItemDefinition"):
    if (
        (i["inventory"].get("tierTypeName") not in results)
        and (ItemCategoryHashes.记忆水晶 in i.get("itemCategoryHashes", []))
        and (
            str(i["displayProperties"]["name"]).startswith(
                i["inventory"]["tierTypeName"]
            )
        )
        and (get("DestinyVendorDefinition", i["hash"]) is not None)
    ):
        results[i["inventory"]["tierTypeName"]] = i["displayProperties"]["icon"]
        logger.debug(
            f"{i['inventory']['tierTypeName']} -> {i['displayProperties']['icon']}"
        )

writeFile("./output/engram-rarity-icons.json", results)
logger.success("writeFile ./output/engram-rarity-icons.json")
logger.info("Generating Engram Rarity icons... Done")
