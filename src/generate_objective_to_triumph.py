import re

from tools import writeFile
from manifest import getAll, loadLocal
from data.generated_enums import ItemCategoryHashes

loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")
records = getAll("DestinyRecordDefinition")

debug = False

objectiveToTriumphHash: dict[int, int] = {}

for item in inventoryItems:
    objectiveHash = item["hash"]
    description = item["displayProperties"]["description"]

    # 确保这是一个任务步骤，因为有些徽章也会追踪目标 (2868525743)
    # 指导你完成一场胜利
    if (
        ItemCategoryHashes.任务步骤 in item.get("itemCategoryHashes", [])
        and re.match(r"完成.+胜利", description)
        and (
            match := re.findall(r'"\W*(\w[^"]+\w)\W*"', description)
        )  # 这里直接抄的原项目，因为这好像是一个废弃的生成脚本，它只会生成一个空文件
    ):
        triumphName = match[1]
        for triumph in records:
            if triumphName == triumph["displayProperties"]["name"]:
                objectiveToTriumphHash[objectiveHash] = triumph["hash"]


writeFile("./output/objective-triumph.json", objectiveToTriumphHash)
