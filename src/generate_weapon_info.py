import ujson
import requests

from log import logger
from tools import writeFile
from manifest import get, getAll, loadLocal
from data.generated_enums import ItemCategoryHashes

loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")
trait = getAll("DestinyTraitCategoryDefinition")
traitType = getAll("DestinyItemTierTypeDefinition")
powerCaps = {i["hash"]: i["powerCap"] for i in getAll("DestinyPowerCapDefinition")}
Stats = getAll("DestinyStatDefinition")

weapons = [
    item
    for item in inventoryItems
    if ItemCategoryHashes.武器 in item.get("itemCategoryHashes", [])
    and ItemCategoryHashes.样品模型 not in item.get("itemCategoryHashes", [])
    and item.get("inventory", {}).get("tierTypeName") in ["传说", "异域"]
]
weaponNames = [i["displayProperties"]["name"] for i in weapons]
weaponsUniq = [
    i for i in weapons if weaponNames.count(i["displayProperties"]["name"]) == 1
]
weaponsDupNames = [
    i["displayProperties"]["name"]
    for i in weapons
    if not weaponNames.count(i["displayProperties"]["name"]) == 1
]
for weaponName in set(weaponsDupNames):
    weaponTwo = [
        i for i in inventoryItems if i["displayProperties"]["name"] == weaponName
    ]
    indexs = [i["index"] for i in weaponTwo]
    weaponsUniq.append(weaponTwo[indexs.index(max(indexs))])


def getSocketInfo(sockets: dict, tierTypeName: str) -> dict:
    global test
    ret: dict = {}
    for socketCategorie in sockets["socketCategories"]:
        socketCategorieName = get(
            "DestinySocketCategoryDefinition", socketCategorie["socketCategoryHash"]
        )["displayProperties"]["name"]
        if socketCategorieName in ["武器模组"] and tierTypeName == "传说":
            continue
        for socketIndex in socketCategorie["socketIndexes"]:
            if sockets["socketEntries"][socketIndex]["singleInitialItemHash"] in [
                4248210736,  # 默认着色器
                2325217837,  # 默认着色器
                0,  # 不知道是啥玩意
                2285418970,  # 记录器
            ]:
                continue
            plugHashs = []
            if plugSetHash := sockets["socketEntries"][socketIndex].get(
                "reusablePlugSetHash"
            ) or sockets["socketEntries"][socketIndex].get("randomizedPlugSetHash"):
                plugSet = get("DestinyPlugSetDefinition", plugSetHash)
                plugHashs = [
                    i["plugItemHash"]
                    for i in plugSet["reusablePlugItems"]
                    if i["currentlyCanRoll"]
                ]
            if (
                sockets["socketEntries"][socketIndex]["singleInitialItemHash"]
                not in plugHashs
            ):
                plugHashs.append(
                    sockets["socketEntries"][socketIndex]["singleInitialItemHash"]
                )
            if reusablePlugItems := sockets["socketEntries"][socketIndex].get(
                "reusablePlugItems"
            ):
                plugHashs.extend(
                    [
                        i["plugItemHash"]
                        for i in reusablePlugItems
                        if i["plugItemHash"] not in plugHashs
                    ]
                )
            if not plugHashs:
                logger.info(
                    "No plugHashs for socketEntries: {}".format(
                        sockets["socketEntries"][socketIndex]
                    )
                )
                continue
            plugs = [
                item["displayProperties"]
                for i in plugHashs
                if (item := get("DestinyInventoryItemDefinition", i))
                and item["displayProperties"]["name"] != "升级大师杰作"
            ]
            if [i for i in plugs if "着色器" in i["description"]]:
                continue
            test = max(test, len(plugs))
            for i in plugs[::-1]:
                if i["name"].endswith("催化"):
                    if recordInfo := get("DestinyRecordDefinition", itemname=i["name"]):
                        i["target"] = recordInfo["displayProperties"]["description"]
                        pluginfo = get("DestinyInventoryItemDefinition", plugHashs[-1])
                        if perks := pluginfo.get("perks"):
                            perkInfos = [
                                get("DestinySandboxPerkDefinition", i["perkHash"])
                                for i in perks
                            ]
                            i["perks"] = [i for i in perkInfos if i["isDisplayable"]]
                        continue
            if not ret.get(socketCategorieName):
                ret[socketCategorieName] = []
            ret[socketCategorieName].append(plugs)
    return ret


test = 0
weaponsData = []
for weapon in weaponsUniq:
    iconWatermark = weapon.get("iconWatermark")
    tierTypeName = weapon["inventory"]["tierTypeName"]
    if quality := weapon.get("quality"):
        if len(quality["versions"]) == 1:
            iconWatermark = quality["displayVersionWatermarkIcons"][0]
        else:
            powerCap = [i["powerCapHash"] for i in quality["versions"]]
            iconWatermark = quality["displayVersionWatermarkIcons"][
                powerCap.index(max(powerCap))
            ]
    stats = {
        statName: v["value"]
        for k, v in weapon["stats"]["stats"].items()
        if (
            statName := get("DestinyStatDefinition", hash=k)
            .get("displayProperties", {})
            .get("name")
        )
        and statName != "能量"
    }
    sockets = getSocketInfo(weapon["sockets"], tierTypeName)
    damageTypes = [
        damageInfo["displayProperties"]
        for i in weapon["damageTypeHashes"]
        if (damageInfo := get("DestinyDamageTypeDefinition", i))
    ]
    weaponsData.append(
        {
            "hash": weapon["hash"],
            "name": weapon["displayProperties"]["name"],
            "icon": weapon["displayProperties"]["icon"],
            "iconWatermark": iconWatermark,
            "secondaryIcon": weapon.get("secondaryIcon"),
            "screenshot": weapon.get("screenshot"),
            "itemTypeDisplayName": weapon["itemTypeDisplayName"],
            "flavorText": weapon.get("flavorText"),
            "stats": stats,
            "ammoType": weapon["equippingBlock"]["ammoType"],
            "sockets": sockets,
            "damageTypes": damageTypes,
            "tierTypeName": tierTypeName,
        }
    )
writeFile(
    "./output/weapon-display-info.json",
    weaponsData,
)
logger.success("writeFile ./output/weapon-display-info.json")
