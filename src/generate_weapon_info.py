import os
from typing import List

import ujson
import requests

from log import logger
from tools import readFile, writeFile, deduplicate
from config import config
from manifest import get, getAll, loadLocal, getManifestOnline
from data.generated_enums import ItemCategoryHashes

version = getManifestOnline()["version"]
# version = "101478.22.01.22.2200-6-bnet.42469"
logger.success("Get Version {}".format(version))

loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")
seasonsInfo = ujson.loads(readFile("./data/seasons/seasons_unfiltered.json"))
extendIch = ujson.loads(readFile("./output/extended-ich.json"))

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
# weaponNames = [i["displayProperties"]["name"] for i in weapons]
# weaponsUniq = [
#     i for i in weapons if weaponNames.count(i["displayProperties"]["name"]) == 1
# ]
# weaponsDupNames = [
#     i["displayProperties"]["name"]
#     for i in weapons
#     if not weaponNames.count(i["displayProperties"]["name"]) == 1
# ]
# for weaponName in set(weaponsDupNames):
#     weaponTwo = [i for i in weapons if i["displayProperties"]["name"] == weaponName]
#     indexs = [i["index"] for i in weaponTwo]
#     weaponsUniq.append(weaponTwo[indexs.index(max(indexs))])


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
            socketEntrie = sockets["socketEntries"][socketIndex]

            # 简单的过滤，着色器数据多会很耗时
            if socketEntrie["singleInitialItemHash"] in [
                4248210736,  # 默认着色器
                2325217837,  # 默认着色器
                2285418970,  # 记录器
            ]:
                continue
            plugHashs = []
            # singleInitialItemHash
            if socketEntrie["singleInitialItemHash"]:
                plugHashs.append(socketEntrie["singleInitialItemHash"])

            # reusablePlugItems
            if reusablePlugItems := socketEntrie.get("reusablePlugItems"):
                plugHashs.extend(
                    [
                        i["plugItemHash"]
                        for i in reusablePlugItems
                        if i["plugItemHash"] not in plugHashs
                    ]
                )

            # reusablePlugSetHash
            if plugSetHash := socketEntrie.get("reusablePlugSetHash"):
                plugHashs.extend(
                    i["plugItemHash"]
                    for i in get("DestinyPlugSetDefinition", plugSetHash)[
                        "reusablePlugItems"
                    ]
                    if i["plugItemHash"] not in plugHashs and i["currentlyCanRoll"]
                )

            # randomizedPlugSetHash
            if plugSetHash := socketEntrie.get("randomizedPlugSetHash"):
                plugHashs.extend(
                    i["plugItemHash"]
                    for i in get("DestinyPlugSetDefinition", plugSetHash)[
                        "reusablePlugItems"
                    ]
                    if i["plugItemHash"] not in plugHashs and i["currentlyCanRoll"]
                )

            # 对plugHashs除去重
            plugHashs = list(deduplicate(plugHashs))

            # 对空plugHashs跳过
            if not plugHashs:
                continue

            # 查询plugHashs详细数据并再次进行筛选，去除大师杰作内容
            plugs = [
                item["displayProperties"]
                for i in plugHashs
                if (item := get("DestinyInventoryItemDefinition", i))
                and item["displayProperties"]["name"] != "升级大师杰作"
            ]

            # 去除未过滤的着色器和记录器内容
            if [i for i in plugs if "着色器" in i["description"]] or [
                i for i in plugs if "记录器" in i["name"]
            ]:
                continue

            # 对催化单独处理
            if plugs[-1]["name"].endswith("催化"):
                # 单独处理催化剂
                if recordInfo := get(
                    "DestinyRecordDefinition", itemname=plugs[-1]["name"]
                ):
                    plugs[-1]["target"] = recordInfo["displayProperties"]["description"]
                    plugs[-1]["step"] = [
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
                    if not ret.get("武器模组"):
                        ret["武器模组"] = []
                    # 催化剂只输出第一个的和最后一个，目前还不清楚为什么有重复的
                    ret["武器模组"].append([plugs[0], plugs[-1]])
                    continue
                else:
                    continue
            # 去重重复名称的perk-特指年5武器的增强perk，后续再决定是否使用，目前先过滤掉
            uniPlugs: List[dict] = []
            for plug in plugs:
                if plug["name"] not in [i["name"] for i in uniPlugs]:
                    uniPlugs.append(plug)
            if not ret.get(socketCategorieName):
                ret[socketCategorieName] = []
            ret[socketCategorieName].append(uniPlugs)
    return ret


weaponsData = []
for weapon in weapons:
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
    # damageTypes = [
    #     damageInfo["displayProperties"]
    #     for i in weapon.get("damageTypeHashes", [])
    #     if (damageInfo := get("DestinyDamageTypeDefinition", i))
    # ]
    if exich := extendIch.get(str(weapon["hash"])):
        weapon["itemCategoryHashes"].append(exich)
    if weapon["itemTypeDisplayName"] == "偃月":
        weapon["itemCategoryHashes"].append(99999999)  # 临时用偃月ich
    weaponsData.append(
        {
            "hash": weapon["hash"],
            "name": weapon["displayProperties"]["name"],
            "icon": weapon["displayProperties"]["icon"],
            "iconWatermark": iconWatermark,
            "secondaryIcon": weapon.get("secondaryIcon"),
            "screenshot": weapon.get("screenshot"),
            "itemTypeDisplayName": weapon["itemTypeDisplayName"],
            "ich": weapon["itemCategoryHashes"],
            "flavorText": weapon.get("flavorText"),
            "stats": stats,
            "ammoType": weapon["equippingBlock"]["ammoType"],
            "sockets": sockets,
            "defaultDamageType": weapon.get("defaultDamageType"),
            "tierTypeName": tierTypeName,
            "sourceString": sourceString,
            "season": seasonsInfo.get(str(weapon["hash"])),
        }
    )

logger.success(f"{version} 生成武器数据 {len(weaponsData)}")

lastData = ujson.loads(readFile("./output/weapon-display-info.json"))
# lastData = []
updateData = [data for data in weaponsData if data not in lastData]
logger.success(f"{version} 更新武器数据 {len(updateData)}")


def uploadWeaponInfo():
    """上传武器信息"""
    url = f"https://test.tianque.top/destiny2/weapon/upload/{version}"
    headers = {"X-TQ-KEY": config.upload_key}
    with requests.Session() as session:
        ret = session.post(url=url, data=ujson.dumps(updateData), headers=headers)
        if ret.status_code == 200:
            logger.success(f"{version} 上传武器信息成功")
        else:
            raise


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
