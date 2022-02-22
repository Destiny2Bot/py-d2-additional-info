import os

import ujson
import requests

from log import logger
from tools import readFile, writeFile
from config import config
from manifest import get, getAll, loadLocal, getManifestOnline
from data.generated_enums import ItemCategoryHashes

version = getManifestOnline()["version"]
logger.success("Get Version {}".format(version))

loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")

# 只提取传说和异域武器
weapons = [
    item
    for item in inventoryItems
    if ItemCategoryHashes.武器 in item.get("itemCategoryHashes", [])
    and ItemCategoryHashes.样品模型 not in item.get("itemCategoryHashes", [])
    and item.get("inventory", {}).get("tierTypeName") in ["传说", "异域"]
]

# 保存原始数据
writeFile(
    f"./output/weapon/weapon-raw-info-{version}.json",
    weapons,
)
logger.success(f"writeFile ./output/weapon/weapon-raw-info-{version}.json")

# 甄别重复名称的武器，对于重复的武器，使用index值更大的一个
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
    ret: dict = {}
    for socketCategorie in sockets["socketCategories"]:
        socketCategorieName = get(
            "DestinySocketCategoryDefinition", socketCategorie["socketCategoryHash"]
        )["displayProperties"]["name"]
        if socketCategorieName in ["武器模组"] and tierTypeName == "传说":
            # 不处理传说武器的模组
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
                # 不需要着色器信息
                continue
            if plugs[-1]["name"].endswith("催化"):
                # 单独处理催化剂
                if recordInfo := get(
                    "DestinyRecordDefinition", itemname=plugs[-1]["name"]
                ):
                    plugs[-1]["target"] = recordInfo["displayProperties"]["description"]
                    plugs[-1]["target2"] = [
                        get("DestinyObjectiveDefinition", i).get("progressDescription")
                        for i in recordInfo["objectiveHashes"]
                    ]
                    itemInfo = get("DestinyInventoryItemDefinition", plugHashs[-1])
                    if perks := itemInfo.get("perks"):
                        plugs[-1]["perks"] = [
                            perk.get("displayProperties")
                            for i in perks
                            if (
                                perk := get(
                                    "DestinySandboxPerkDefinition", i["perkHash"]
                                )
                            )
                            and perk.get("isDisplayable")
                        ]
                    if investmentStats := itemInfo.get("investmentStats"):
                        plugs[-1]["investmentStats"] = {
                            statName: i["value"]
                            for i in investmentStats
                            if (
                                statName := get(
                                    "DestinyStatDefinition", hash=i["statTypeHash"]
                                )
                                .get("displayProperties", {})
                                .get("name")
                            )
                        }
                else:
                    continue
            if not ret.get(socketCategorieName):
                ret[socketCategorieName] = []
            ret[socketCategorieName].append(plugs)
    return ret


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
    sourceString = ""
    if collectibleHash := weapon.get("collectibleHash"):
        sourceString = get("DestinyCollectibleDefinition", collectibleHash).get(
            "sourceString", ""
        )
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
            "sourceString": sourceString,
        }
    )

logger.success(f"{version} 生成武器数据 {len(weaponsData)}")

lastData = ujson.loads(readFile("./output/weapon-display-info.json"))
updateData = [data for data in weaponsData if data not in lastData]
logger.success(f"{version} 更新武器数据 {len(updateData)}")


def uploadWeaponInfo():
    """上传武器信息"""
    if os.environ.get("UPLOAD_URL") != os.environ.get("UPLOAD_KEY"):
        print("PL")
    url = f"{os.environ.get('UPLOAD_URL')}{version}"
    print(url, os.environ.get("UPLOAD_KEY"))
    headers = {"X-TQ-KEY": os.environ.get("UPLOAD_KEY")}
    with requests.Session() as session:
        ret = session.post(url=url, data=ujson.dumps(updateData), headers=headers)
        if ret.status_code == 200:
            logger.success(f"{version} 上传武器信息成功")


if updateData:
    uploadWeaponInfo()


writeFile(
    "./output/weapon-display-info.json",
    weaponsData,
)
logger.success("writeFile ./output/weapon-display-info.json")

writeFile(
    f"./output/weapon/weapon-display-info-{version}.json",
    weaponsData,
)
logger.success(f"writeFile ./output/weapon/weapon-display-info-{version}.json")
