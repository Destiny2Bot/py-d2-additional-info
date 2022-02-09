from enum import IntEnum

class D2EventEnum(IntEnum):
    曙光节 = 1
    血色浪漫 = 2
    至日英雄 = 3
    英灵日 = 4
    狂欢季节 = 5
    守护者游戏 = 6


D2EventInfo = {
    1: {
        "name": "曙光节",
        "shortname": "曙光节",
        "sources": [4054646289, 3952847349, 930411416, 510530151],
        "engram": [3151770741],
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
        "sources": [641018908, 3724111213, 151416041],
        "engram": [821844118],
    },
    4: {
        "name": "英灵日",
        "shortname": "英灵日",
        "sources": [1919933822, 1677921161, 3190938946, 1054169368, 3693722471],
        "engram": [1451959506],
    },
    5: {
        "name": "狂欢季节",
        "shortname": "欢庆",
        "sources": [2187511136],
        "engram": [],
    },
    6: {
        "name": "守护者游戏",
        "shortname": "游戏",
        "sources": [611838069, 2011810450, 3388021959],
        "engram": [],
    },

}

D2EventPredicateLookup = {
    "曙光节": D2EventEnum.曙光节,
    "血色浪漫": D2EventEnum.血色浪漫,
    "至日": D2EventEnum.至日英雄,
    "英灵日": D2EventEnum.英灵日,
    "欢庆": D2EventEnum.狂欢季节,
    "游戏": D2EventEnum.守护者游戏,

}

D2SourcesToEvent = {
    4054646289: D2EventEnum.曙光节,
    3952847349: D2EventEnum.曙光节,
    930411416: D2EventEnum.曙光节,
    510530151: D2EventEnum.曙光节,
    2502262376: D2EventEnum.血色浪漫,
    641018908: D2EventEnum.至日英雄,
    3724111213: D2EventEnum.至日英雄,
    151416041: D2EventEnum.至日英雄,
    1919933822: D2EventEnum.英灵日,
    1677921161: D2EventEnum.英灵日,
    3190938946: D2EventEnum.英灵日,
    1054169368: D2EventEnum.英灵日,
    3693722471: D2EventEnum.英灵日,
    2187511136: D2EventEnum.狂欢季节,
    611838069: D2EventEnum.守护者游戏,
    2011810450: D2EventEnum.守护者游戏,
    3388021959: D2EventEnum.守护者游戏,

}