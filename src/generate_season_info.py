from typing import TYPE_CHECKING

from manifest import getAll, loadLocal
from tools.JsonIO import readjson, writejson
from tools import copyFile, deduplication
from data.seasons.d2_season_info import D2CalculatedSeason, D2SeasonInfo


# 这里面是表里所有内容于哪个赛季添加的记录
seasons: dict[str, int] = readjson('./data/seasons/seasons_unfiltered.json')

loadLocal()

inventoryItems = getAll('DestinyInventoryItemDefinition')
powerCaps = [i['powerCap'] for i in getAll('DestinyPowerCapDefinition') if i['powerCap'] > 1000 and i['powerCap'] < 50000]
# 对  powerCaps 在保留顺序的情况下进行去重
powerCaps = deduplication(powerCaps)

# 将新增的内容标记到当前赛季
for i in inventoryItems:
    hash = str(i['hash'])
    if hash not in seasons.keys():
        seasons[hash] = D2CalculatedSeason

# 写回
writejson('./data/seasons/seasons_unfiltered.json', seasons)

# 一个新的字典内容为 dict[赛季简称: 赛季编号]
seasonTags = {i.seasonTag: i.season for i in D2SeasonInfo.values() if i.season > 0 and i.seasonTag}
writejson('./output/season-tags.json', seasonTags)

if TYPE_CHECKING:
    from data.seasons.d2_season_info import D2SeasonInfoItem

def checkIsRealSeason(seasonInfo: "D2SeasonInfoItem") -> bool:
    isRealSeason = seasonInfo.season > 0 and seasonInfo.season <= D2CalculatedSeason
    # 将已存在的最大光等从 powerCaps 中删除
    if isRealSeason and seasonInfo.pinnacleCap in powerCaps:
        powerCaps.remove(seasonInfo.pinnacleCap)
    return isRealSeason

lightCapToSeason = {i.pinnacleCap:i.season for i in D2SeasonInfo.values() if checkIsRealSeason(i)}

# 对余下的光等内容推断为后续赛季
for season, powerCap in enumerate(powerCaps, D2CalculatedSeason + 1) :
    lightCapToSeason[powerCap] = season

writejson('./output/lightcap-to-season.json', lightCapToSeason)
copyFile('./data/seasons/d2_season_info.py', './output/d2_season_info.py')