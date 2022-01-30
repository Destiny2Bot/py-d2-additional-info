# stolen from bungieapi/generated/components/schemas/destiny/__init__.py
from enum import Enum

class DestinySocketCategoryStyle(Enum):
    """表示游戏用于渲染 Socket 类别的可能和已知的 UI 样式。"""

    UNKNOWN = 0
    REUSABLE = 1
    CONSUMABLE = 2
    UNLOCKABLE = 3
    INTRINSIC = 4
    ENERGY_METER = 5
    LARGE_PERK = 6
    ABILITIES = 7
    SUPERS = 8

class DestinyItemType(Enum):
    """一个表示物品的高级 "类型 "的枚举，试图为一个实体的具体实例消除上下文的差异。
    例如，尽管一个武器可能有各种武器 "类型"，但在DestinyItemType中，它们都被归类为 "武器"。
    这允许在更高的抽象层次上对类型的概念进行更好的过滤。

    NOTE: 这并不是所有的物品类型，其中一些是《命运1》中遗留下来的，可能存在也可能不存在。我一直在更新这些东西，因为它们太他妈的方便了。我想我不应该与之抗争。。
    """

    NONE = 0
    CURRENCY = 1
    ARMOR = 2
    WEAPON = 3
    MESSAGE = 7
    ENGRAM = 8
    CONSUMABLE = 9
    EXCHANGE_MATERIAL = 10
    MISSION_REWARD = 11
    QUEST_STEP = 12
    QUEST_STEP_COMPLETE = 13
    EMBLEM = 14
    QUEST = 15
    SUBCLASS = 16
    CLAN_BANNER = 17
    AURA = 18
    MOD = 19
    DUMMY = 20
    SHIP = 21
    VEHICLE = 22
    EMOTE = 23
    GHOST = 24
    PACKAGE = 25
    BOUNTY = 26
    WRAPPER = 27
    SEASONAL_ARTIFACT = 28
    FINISHER = 29

class DestinyItemSubType(Enum):
    """这个枚举通过比DestinyItemType更具体的分类来进一步对项目进行分类。
    子类型 "是我们对物品的分类和归类在具体性上更进一步的地方。
    例如，"自动步枪 "而不仅仅是 "武器"，或者 "先锋赏金 "而不仅仅是 "赏金"。

    NOTE: 这并不是所有可用的物品类型，其中一些是《命运1》中遗留下来的，可能存在也可能不存在。
    """

    NONE = 0
    CRUCIBLE = (
        1  # DEPRECATED. Items can be both "Crucible" and something else interesting.
    )
    VANGUARD = 2  # DEPRECATED. An item can both be "Vanguard" and something else.
    EXOTIC = 5  # DEPRECATED. An item can both be Exotic and something else.
    AUTO_RIFLE = 6
    SHOTGUN = 7
    MACHINEGUN = 8
    HAND_CANNON = 9
    ROCKET_LAUNCHER = 10
    FUSION_RIFLE = 11
    SNIPER_RIFLE = 12
    PULSE_RIFLE = 13
    SCOUT_RIFLE = 14
    CRM = 16  # DEPRECATED. An item can both be CRM and something else.
    SIDEARM = 17
    SWORD = 18
    MASK = 19
    SHADER = 20
    ORNAMENT = 21
    FUSION_RIFLE_LINE = 22
    GRENADE_LAUNCHER = 23
    SUBMACHINE_GUN = 24
    TRACE_RIFLE = 25
    HELMET_ARMOR = 26
    GAUNTLETS_ARMOR = 27
    CHEST_ARMOR = 28
    LEG_ARMOR = 29
    CLASS_ARMOR = 30
    BOW = 31
    DUMMY_REPEATABLE_BOUNTY = 32

class BucketCategory(Enum):
    """这个枚举表示一个物品的类别。"""
    
    INVISIBLE = 0
    ITEM = 1
    CURRENCY = 2
    EQUIPPABLE = 3
    IGNORED = 4

DestinySocketCategoryStyleLookup = {v.value:v.name for v in DestinySocketCategoryStyle}
DestinyItemTypeLookup = {v.value:v.name for v in DestinyItemType}
DestinyItemSubTypeLookup = {v.value:v.name for v in DestinyItemSubType}
BucketCategoryLookup = {v.value:v.name for v in BucketCategory}