from enum import IntEnum


class D2EventEnum(IntEnum):
    曙光节 = 1
    血色浪漫 = 2
    至日 = 3
    英灵日 = 4
    欢庆 = 5
    游戏 = 6


D2EventInfo = {
    1: {
        "name": "曙光节",
        "shortname": "曙光节",
        "sources": [464727567, 547767158, 629617846, 2364515524, 3092212681, 3952847349, 4054646289],
        "engram": [1170720694, 3151770741],
    },
    2: {
        "name": "血色浪漫",
        "shortname": "血色浪漫",
        "sources": [2502262376],
        "engram": [3373123597, 191363032],
    },
    3: {
        "name": "至日英雄",
        "shortname": "至日",
        "sources": [],
        "engram": [821844118],
    },
    4: {
        "name": "英灵日",
        "shortname": "英灵日",
        "sources": [1054169368, 1677921161, 1919933822, 3190938946, 3693722471, 4041583267],
        "engram": [1451959506],
    },
    5: {
        "name": "狂欢季节",
        "shortname": "欢庆",
        "sources": [2187511136],
        "engram": [2570200927, 1974821348],
    },
    6: {
        "name": "守护者游戏",
        "shortname": "游戏",
        "sources": [611838069, 2006303146, 2011810450, 2473294025, 3388021959],
        "engram": [],
    },

}

D2EventPredicateLookup = {
    "曙光节": D2EventEnum.曙光节,
    "血色浪漫": D2EventEnum.血色浪漫,
    "至日": D2EventEnum.至日,
    "英灵日": D2EventEnum.英灵日,
    "欢庆": D2EventEnum.欢庆,
    "游戏": D2EventEnum.游戏,

}

D2SourcesToEvent = {
    464727567: D2EventEnum.曙光节,
    547767158: D2EventEnum.曙光节,
    629617846: D2EventEnum.曙光节,
    2364515524: D2EventEnum.曙光节,
    3092212681: D2EventEnum.曙光节,
    3952847349: D2EventEnum.曙光节,
    4054646289: D2EventEnum.曙光节,
    2502262376: D2EventEnum.血色浪漫,
    1054169368: D2EventEnum.英灵日,
    1677921161: D2EventEnum.英灵日,
    1919933822: D2EventEnum.英灵日,
    3190938946: D2EventEnum.英灵日,
    3693722471: D2EventEnum.英灵日,
    4041583267: D2EventEnum.英灵日,
    2187511136: D2EventEnum.欢庆,
    611838069: D2EventEnum.游戏,
    2006303146: D2EventEnum.游戏,
    2011810450: D2EventEnum.游戏,
    2473294025: D2EventEnum.游戏,
    3388021959: D2EventEnum.游戏,

}