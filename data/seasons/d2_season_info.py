from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class D2SeasonEnum(Enum):
    猩红战争 = 1
    冥王诅咒 = 2
    复苏 = 3
    恶徒赛季 = 4
    锻炉赛季 = 5
    浪客赛季 = 6
    丰盈赛季 = 7
    不朽赛季 = 8
    黎明赛季 = 9
    英杰赛季 = 10
    影临赛季 = 11
    狂猎赛季 = 12
    天选赛季 = 13
    永夜赛季 = 14
    神隐赛季 = 15
    隐藏赛季 = 16

D2SeasonInfoDict_nomodel = {
    1: {
      'DLCName': '猩红战争',
      'seasonName': '猩红战争',
      'seasonTag': '猩红战争',
      'season': 1,
      'maxLevel': 20,
      'powerFloor': 0,
      'softCap': 285,
      'powerfulCap': 300,
      'pinnacleCap': 300,
      'releaseDate': '2017-09-06',
      'resetTime': '09:00:00Z',
      'numWeeks': 13,
    },
    2: {
      'DLCName': '冥王诅咒',
      'seasonName': '冥王诅咒',
      'seasonTag': '冥王诅咒',
      'season': 2,
      'maxLevel': 25,
      'powerFloor': 0,
      'softCap': 320,
      'powerfulCap': 330,
      'pinnacleCap': 330,
      'releaseDate': '2017-12-05',
      'resetTime': '17:00:00Z',
      'numWeeks': 22,
    },
    3: {
      'DLCName': '战争思维',
      'seasonName': '复苏',
      'seasonTag': '战争思维',
      'season': 3,
      'maxLevel': 30,
      'powerFloor': 0,
      'softCap': 340,
      'powerfulCap': 380,
      'pinnacleCap': 380,
      'releaseDate': '2018-05-08',
      'resetTime': '18:00:00Z',
      'numWeeks': 17,
    },
    4: {
      'DLCName': '遗落之族',
      'seasonName': '恶徒赛季',
      'seasonTag': '恶徒',
      'season': 4,
      'maxLevel': 50,
      'powerFloor': 0,
      'softCap': 500,
      'powerfulCap': 600,
      'pinnacleCap': 600,
      'releaseDate': '2018-09-04',
      'resetTime': '17:00:00Z',
      'numWeeks': 13,
    },
    5: {
      'DLCName': '黑色军火库',
      'seasonName': '锻炉赛季',
      'seasonTag': '锻炉',
      'season': 5,
      'maxLevel': 50,
      'powerFloor': 0,
      'softCap': 500,
      'powerfulCap': 650,
      'pinnacleCap': 650,
      'releaseDate': '2018-11-27',
      'resetTime': '17:00:00Z',
      'numWeeks': 12,
    },
    6: {
      'DLCName': "Joker's Wild",
      'seasonName': '浪客赛季',
      'seasonTag': '浪客',
      'season': 6,
      'maxLevel': 50,
      'powerFloor': 0,
      'softCap': 500,
      'powerfulCap': 700,
      'pinnacleCap': 700,
      'releaseDate': '2019-03-05',
      'resetTime': '17:00:00Z',
      'numWeeks': 14,
    },
    7: {
      'DLCName': '飘渺半影',
      'seasonName': '丰盈赛季',
      'seasonTag': '丰盈',
      'season': 7,
      'maxLevel': 50,
      'powerFloor': 0,
      'softCap': 500,
      'powerfulCap': 750,
      'pinnacleCap': 750,
      'releaseDate': '2019-06-04',
      'resetTime': '17:00:00Z',
      'numWeeks': 13,
    },
    8: {
      'DLCName': '暗影要塞',
      'seasonName': '不朽赛季',
      'seasonTag': '不朽',
      'season': 8,
      'maxLevel': 50,
      'powerFloor': 750,
      'softCap': 900,
      'powerfulCap': 950,
      'pinnacleCap': 960,
      'releaseDate': '2019-10-01',
      'resetTime': '17:00:00Z',
      'numWeeks': 10,
    },
    9: {
      'DLCName': '',
      'seasonName': '黎明赛季',
      'seasonTag': '黎明',
      'season': 9,
      'maxLevel': 50,
      'powerFloor': 750,
      'softCap': 900,
      'powerfulCap': 960,
      'pinnacleCap': 970,
      'releaseDate': '2019-12-10',
      'resetTime': '17:00:00Z',
      'numWeeks': 13,
    },
    10: {
      'DLCName': '',
      'seasonName': '英杰赛季',
      'seasonTag': '英杰',
      'season': 10,
      'maxLevel': 50,
      'powerFloor': 750,
      'softCap': 950,
      'powerfulCap': 1000,
      'pinnacleCap': 1010,
      'releaseDate': '2020-03-10',
      'resetTime': '17:00:00Z',
      'numWeeks': 13,
    },
    11: {
      'DLCName': '',
      'seasonName': '影临赛季',
      'seasonTag': '影临',
      'season': 11,
      'maxLevel': 50,
      'powerFloor': 750,
      'softCap': 1000,
      'powerfulCap': 1050,
      'pinnacleCap': 1060,
      'releaseDate': '2020-06-09',
      'resetTime': '17:00:00Z',
      'numWeeks': 15,
    },
    12: {
      'DLCName': '凌光之刻',
      'seasonName': '狂猎赛季',
      'seasonTag': '狂猎',
      'season': 12,
      'maxLevel': 50,
      'powerFloor': 1050,
      'softCap': 1200,
      'powerfulCap': 1250,
      'pinnacleCap': 1260,
      'releaseDate': '2020-11-10',
      'resetTime': '17:00:00Z',
      'numWeeks': 12,
    },
    13: {
      'DLCName': '',
      'seasonName': '天选赛季',
      'seasonTag': '天选',
      'season': 13,
      'maxLevel': 50,
      'powerFloor': 1100,
      'softCap': 1250,
      'powerfulCap': 1300,
      'pinnacleCap': 1310,
      'releaseDate': '2021-02-09',
      'resetTime': '17:00:00Z',
      'numWeeks': 13,
    },
    14: {
      'DLCName': '',
      'seasonName': '永夜赛季',
      'seasonTag': '永夜',
      'season': 14,
      'maxLevel': 50,
      'powerFloor': 1100,
      'softCap': 1250,
      'powerfulCap': 1310,
      'pinnacleCap': 1320,
      'releaseDate': '2021-05-11',
      'resetTime': '17:00:00Z',
      'numWeeks': 15,
    },
    15: {
      'DLCName': '',
      'seasonName': '神隐赛季',
      'seasonTag': '神隐',
      'season': 15,
      'maxLevel': 50,
      'powerFloor': 1100,
      'softCap': 1250,
      'powerfulCap': 1320,
      'pinnacleCap': 1330,
      'releaseDate': '2021-08-24',
      'resetTime': '17:00:00Z',
      'numWeeks': 26,
    },
    16: {
      'DLCName': '邪姬魅影',
      'seasonName': '【隐藏】赛季',
      'seasonTag': '邪姬魅影',
      'season': 16,
      'maxLevel': 50,
      'powerFloor': 1350,
      'softCap': 1500,
      'powerfulCap': 1550,
      'pinnacleCap': 1560,
      'releaseDate': '2022-02-22',
      'resetTime': '17:00:00Z',
      'numWeeks': 15,
    },
}

class D2SeasonInfoItem(BaseModel):
    DLCName: str
    seasonName: str
    seasonTag: str
    season: int
    maxLevel: int
    powerFloor: int
    softCap: int
    powerfulCap: int
    pinnacleCap: int
    releaseDate: str
    resetTime: str
    numWeeks: int

    class Config:
      frozen=True

D2SeasonInfo:dict[int, D2SeasonInfoItem] = {}
for key, value in D2SeasonInfoDict_nomodel.items():
  D2SeasonInfo[key] = D2SeasonInfoItem(**value)

del D2SeasonInfoDict_nomodel



def getCurrentSeason() -> int:
  CLOSE_TO_RESET_HOURS = 5
  today = datetime.now()
  for i in range(len(D2SeasonEnum),0,-1):
    seasonDate = datetime.strptime(f'{D2SeasonInfo[i].releaseDate} {D2SeasonInfo[i].resetTime}', '%Y-%m-%d %H:%M:%S%z')
    seasonDate = seasonDate.astimezone().replace(tzinfo=None) # 转换为无时区信息的中国标准时间

    # 如果当前时间大于赛季开始时间或距离赛季开始时间小于5小时，则返回当前赛季
    closeToNewSeason = isToday(seasonDate) and numHoursBetween(today, seasonDate) < CLOSE_TO_RESET_HOURS
    if today >= seasonDate or closeToNewSeason:
      return D2SeasonInfo[i].season
  return 0

def numHoursBetween(d1: datetime, d2: datetime):
  SECONDS_PER_HOUR = 3600
  return abs((d1 - d2).total_seconds() // SECONDS_PER_HOUR)


def isToday(someDate: datetime):
  today = datetime.now()
  return (today.year == someDate.year and today.month == someDate.month and today.day == someDate.day)

D2CalculatedSeason: int = getCurrentSeason()
