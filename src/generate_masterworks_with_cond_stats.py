from tools import writeFile
from manifest import getAll, loadLocal

loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")

masterworkPlugsWithCondStats = [
    i["hash"]
    for i in inventoryItems
    if i["displayProperties"]["name"] == "大师杰作"
    and any([s for s in i.get("investmentStats", []) if s.get("isConditionallyActive")])
]

masterworkPlugsWithCondStats.sort()

# 输出大师杰作模组(附加属性)
writeFile("./output/masterworks-with-cond-stats.json", masterworkPlugsWithCondStats)
