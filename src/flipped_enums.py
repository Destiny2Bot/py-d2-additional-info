# stolen from bungieapi/generated/components/schemas/destiny/__init__.py

from bungieapi.generated.components.schemas.destiny import (
    BucketCategory,
    DestinyItemType,
    DestinyItemSubType,
    DestinySocketCategoryStyle,
)

# 直接从 bungieapi 引入他不香吗，不过我觉得需要保留中文注释
_docs = {
    "DestinySocketCategoryStyle": "表示游戏用于渲染 Socket 类别的可能和已知的 UI 样式。",
    "DestinyItemType": """
    一个表示物品的高级 '类型' 的枚举，试图为一个实体的具体实例消除上下文的差异。
    例如，尽管一个武器可能有各种武器 '类型'，但在DestinyItemType中，它们都被归类为 '武器'
    这允许在更高的抽象层次上对类型的概念进行更好的过滤。
    NOTE: 这并不是所有的物品类型，其中一些是《命运1》中遗留下来的，可能存在也可能不存在。
    我一直在更新这些东西，因为它们太他妈的方便了。我想我不应该与之抗争。
    """,
    "DestinyItemSubType": """
    这个枚举通过比DestinyItemType更具体的分类来进一步对项目进行分类。
    子类型 "是我们对物品的分类和归类在具体性上更进一步的地方。
    例如，"自动步枪 "而不仅仅是 "武器"，或者 "先锋赏金 "而不仅仅是 "赏金"。
    NOTE: 这并不是所有可用的物品类型，其中一些是《命运1》中遗留下来的，可能存在也可能不存在。
    """,
    "DestinyBucketCategory": """这个枚举表示一个物品的类别。""",
}


DestinySocketCategoryStyleLookup = {v.value: v.name for v in DestinySocketCategoryStyle}
DestinyItemTypeLookup = {v.value: v.name for v in DestinyItemType}
DestinyItemSubTypeLookup = {v.value: v.name for v in DestinyItemSubType}
BucketCategoryLookup = {v.value: v.name for v in BucketCategory}
