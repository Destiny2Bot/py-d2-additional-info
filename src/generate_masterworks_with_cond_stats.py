from log import logger
from tools import writeFile
from manifest import getAll, loadLocal

logger.info("Generating Masterworks with Cond Stats... 大师杰作模组(附加属性)")
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
logger.success("writeFile ./output/masterworks-with-cond-stats.json")
logger.info("Generating Masterworks with Cond Stats... Done")
