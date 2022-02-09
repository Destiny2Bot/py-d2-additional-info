from typing import Any, List

import ujson

from log import logger
from tools import copyFile, readFile, writeFile, deduplicate
from manifest import get, getAll, loadLocal
from data.generated_enums import ItemCategoryHashes
from data.seasons.d2_season_info import D2CalculatedSeason

seasonsUnfiltered: dict[str, int] = ujson.loads(
    readFile("./data/seasons/seasons_unfiltered.json")
)

logger.info("Generating Season To Source...")
loadLocal()

inventoryItems: Any = getAll("DestinyInventoryItemDefinition")

# 赛季编号
seasonNumbers = [i for i in range(1, D2CalculatedSeason + 1)]

# 赛季编号对来源信息的映射
seasonToSource: dict[int, List[int]] = {}

# 初始化 seasonToSource
for i in seasonNumbers:
    seasonToSource[i] = []

# 道具 hash 对道具来源信息的映射
itemSource: dict[int, int] = {}

for item in inventoryItems:
    # 找出有来源信息的道具
    collectibleHash = item.get("collectibleHash")
    if not collectibleHash:
        continue

    # 去来源信息表核对
    collectibleinfo = get("DestinyCollectibleDefinition", collectibleHash)
    if not collectibleinfo:
        continue

    sourceHash = collectibleinfo["sourceHash"]
    season = seasonsUnfiltered.get(str(item["hash"]))

    if sourceHash and season:
        seasonToSource[season].append(sourceHash)
        itemSource[item["hash"]] = sourceHash

# seasonToSource 去重
for season in seasonNumbers:
    seasonToSource[season] = list(deduplicate(seasonToSource[season]))

# 验证是否有交集，如果有则从 seasonToSource 中去除

# notSeasonallyUnique 中包含来自于多个赛季的项目的源哈希
notSeasonallyUnique: List[int] = []
for seasonA in seasonNumbers:
    for seasonB in range(seasonA + 1, D2CalculatedSeason + 1):
        notSeasonallyUnique.extend(
            list(set(seasonToSource[seasonA]) & set(seasonToSource[seasonB]))
        )

# notSeasonallyUnique 去重
notSeasonallyUnique = list(deduplicate(notSeasonallyUnique))

# 从 seasonToSource 中删除 notSeasonallyUnique 中的条目
for season in seasonNumbers:
    seasonToSource[season] = list(set(seasonToSource[season]) - set(notSeasonallyUnique))
    seasonToSource[season].sort()

categoryDenyList = [
    ItemCategoryHashes.货币.value,
    ItemCategoryHashes.记忆水晶.value,
    ItemCategoryHashes.材料.value,
    ItemCategoryHashes.公会战旗_CLAN_BANNER.value,
    ItemCategoryHashes.包裹.value,
    ItemCategoryHashes.奖励模组.value,
    ItemCategoryHashes.武器模组弓弦.value,
    ItemCategoryHashes.武器模组游戏.value,
    ItemCategoryHashes.武器模组电池.value,
    ItemCategoryHashes.机灵模组.value,
    ItemCategoryHashes.公会战旗特性.value,
    ItemCategoryHashes.武器模组剑刃.value,
    ItemCategoryHashes.预言贡品.value,
    ItemCategoryHashes.武器模组发射管.value,
    ItemCategoryHashes.恶搞奖品.value,
    ItemCategoryHashes.武器模组固有.value,
    ItemCategoryHashes.预言石板.value,
    ItemCategoryHashes.藏宝图.value,
    ItemCategoryHashes.武器模组瞄准镜.value,
    ItemCategoryHashes.物品套装.value,
    ItemCategoryHashes.武器模组枪托.value,
    ItemCategoryHashes.武器模组护手.value,
    ItemCategoryHashes.武器模组枪管.value,
    ItemCategoryHashes.样品模型.value,
    ItemCategoryHashes.武器模组箭矢.value,
    ItemCategoryHashes.武器模组框架.value,
    ItemCategoryHashes.武器模组握把.value,
    ItemCategoryHashes.武器模组准心.value,
    ItemCategoryHashes.武器模组弹匣.value,
]

# 来源 hash 到赛季的映射
sources: dict[int, int] = {}
for season in seasonToSource.keys():
    for source in seasonToSource[season]:
        sources[source] = int(season)
        logger.debug(f"{source} : {season}")

seasonToSourceOutput = {
    "categoryDenyList": categoryDenyList,
    "sources": sources,
}

writeFile("./output/season-to-source.json", seasonToSourceOutput)
logger.success("writeFile ./output/season-to-source.json")

seasons: dict[int, int] = {}

# 获取没有赛季图标的道具
inventoryItems = [
    i
    for i in inventoryItems
    if i.get("quality")
    and (
        not i["quality"].get("displayVersionWatermarkIcons")
        or "" in i["quality"].get("displayVersionWatermarkIcons")
    )
]

for item in inventoryItems:
    categoryHashes = item.get("itemCategoryHashes", [])
    seasonDenied = len([i for i in categoryDenyList if i in categoryHashes])
    if (
        (
            itemSource.get(item["hash"]) in notSeasonallyUnique
            or not itemSource.get(item["hash"])
        )
        and not seasonDenied
        and (item.get("itemTypeDisplayName") or len(categoryHashes))
    ):
        seasons[item["hash"]] = seasonsUnfiltered[str(item["hash"])]


def removeItemsNoLongerInManifest(seasons: dict[int, int]) -> dict[int, int]:
    hashesManifest: List[str] = []
    hashesSeason: List[str] = []
    deleted = 0
    matches = 0
    for item in inventoryItems:
        # 存储了所有没有赛季图标的道具的 hash
        hashesManifest.append(str(item["hash"]))
    for key in seasons.keys():
        # 存储了过滤后的道具hash
        hashesSeason.append(str(key))

    # 去除所有不在未过滤集中的道具
    # 天阙：什么时候会出现去除的情况呢？seasonsUnfiltered里面出现过期道具
    for hash in hashesSeason:
        if hash in hashesManifest:
            matches += 1
        else:
            deleted += 1
            seasons.pop(int(hash))
    logger.info(f"{matches} matches out of {len(hashesSeason)} hashes.")
    logger.info(f"Deleted {deleted} items.")
    return seasons


seasonsClean = removeItemsNoLongerInManifest(seasons)

# 这里面存了没有赛季图标的道具赛季信息（由每次 manifest 更新自动生成）
writeFile("./output/seasons.json", seasonsClean)
logger.success("writeFile ./output/seasons.json")
logger.info("Generating Season To Source... Done")
