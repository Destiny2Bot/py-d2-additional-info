from typing import List

from log import logger
from tools import writeFile, dedupeAndSortArray
from manifest import getAll, loadLocal

loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")
milestones = getAll("DestinyMilestoneDefinition")

rewards: List[int] = []
rewardHash = "326786556"

debug = False

# 将高光任务加入输出
for milestone in milestones:
    reward = None
    if rewardss := milestone.get("rewards"):
        if target := rewardss.get(rewardHash):
            if entries := target.get("rewardEntries"):
                reward = entries["326786556"]["items"][0]["itemHash"]

    if reward and reward != 3853748946:
        if debug:
            logger.info(milestone["rewards"][rewardHash]["rewardEntries"][rewardHash])
        rewards.append(reward)

    questHash = int(list(quests.keys())[0]) if (quests := milestone.get("quests")) else 0
    for item in inventoryItems:
        questReward = None
        if item.get("hash") == questHash:
            if not item.get("setData", {}).get("setIsFeatured"):
                questReward = None
                if value := item.get("value"):
                    questReward = value.get("itemValue")[0]["itemHash"]
        if questReward:
            rewards.append(questReward)

# 将高光球加入输出
for item in inventoryItems:
    hash = item["hash"]
    powerfulEquipment = "解密大师可将它解码成一件强大的装备"
    if powerfulEquipment in item["displayProperties"]["description"]:
        if debug:
            logger.info(item["displayProperties"]["name"])
        rewards.append(hash)

# 去重
cleanedRewards = dedupeAndSortArray(rewards)

# 输出所有高光奖励
writeFile("./output/powerful-rewards.json", cleanedRewards)
