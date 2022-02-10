from typing import List

from log import logger
from tools import writeFile, sortObject
from manifest import get, loadLocal

logger.info('Generating spider mats...蛛王售卖信息')

loadLocal()

spiderMatsWithIndex: List[dict] = []
spiderMats: List[int] = []

DENY_HASHES = [1022552290]

GLIMMER_HASHES = [3159615086, 3664001560]
indexFixList = ["相位琉璃锋针", "重子树枝"]
spider = get("DestinyVendorDefinition", 863940356)

if itemList := spider.get("itemList"):
    for i in itemList:
        if i["itemHash"] in GLIMMER_HASHES:
            if i["currencies"][0]["itemHash"] not in DENY_HASHES:
                item = get(
                    "DestinyInventoryItemDefinition", i["currencies"][0]["itemHash"]
                )
                hash = item["hash"]
                name = item["displayProperties"]["name"]
                index = item["index"]
                if not any([j for j in spiderMatsWithIndex if j.get("hash") == hash]):
                    spiderMatsWithIndex.append(
                        {
                            "hash": hash,
                            "index": index + 16
                            if any(iFix for iFix in indexFixList if iFix in name)
                            else index,
                        }
                    )

spiderMatsWithIndex.sort(key=lambda x: x["index"])

spiderMats = [i["hash"] for i in spiderMatsWithIndex]

validSpiderCurrencies = []

if itemList := spider.get("itemList"):
    for i in itemList:
        for c in i.get("currencies"):
            itemHash = c.get("itemHash")
            name = get("DestinyInventoryItemDefinition", itemHash)["displayProperties"][
                "name"
            ]
            validSpiderCurrencies.append([itemHash, name])
purchaseableCurrencyItems = []
if itemList := spider.get("itemList"):
    for i in itemList:
        itemName: str = get("DestinyInventoryItemDefinition", i["itemHash"])[
            "displayProperties"
        ]["name"]
        if itemName.startswith("购买"):
            for _, matName in validSpiderCurrencies:
                if itemName.replace("购买", "") in matName or (
                    matName and matName in itemName
                ):
                    purchaseableCurrencyItems.append(i)
purchaseableMatTable: dict[int, int] = {}
for i in purchaseableCurrencyItems:
    itemNames: str = get("DestinyInventoryItemDefinition", i["itemHash"])[
        "displayProperties"
    ]["name"]
    purchaseableMatTable[i["itemHash"]] = [
        i
        for i, matName in validSpiderCurrencies
        if itemNames.replace("购买", "") in matName or (matName and matName in itemNames)
    ][0]
purchaseableMatTable = sortObject(purchaseableMatTable)

# 蛛王出售物品的 hash
writeFile("./output/spider-mats.json", spiderMats)
logger.success("writeFile ./output/spider-mats.json")

# 蛛王出售物品的购买材料信息，表项为 物品: 所需材料
writeFile("./output/spider-purchaseables-to-mats.json", purchaseableMatTable)
logger.success("writeFile ./output/spider-purchaseables-to-mats.json")
logger.info('Generating spider mats...Done')
