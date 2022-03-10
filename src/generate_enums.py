from typing import Any, Dict, List

from log import logger
from tools import writeFile, deduplicate
from manifest import getAll, loadLocal
from src.flipped_enums import (
    BucketCategoryLookup,
    DestinyItemTypeLookup,
    DestinyItemSubTypeLookup,
    DestinySocketCategoryStyleLookup,
)

logger.info("Generating Enums... 需要用到的枚举类")
loadLocal()

ignoreHashes = [
    3792382831,  # SocketCategory "Ingredients" -- nothing corresponds to this. 322810736 is the right one
    2481496894,  # SocketCategory "Recipes" -- nothing corresponds to this. 2059652296 is the right one
]

generatedEnums: dict[str, dict[str, int]] = {}

inventoryItems = getAll("DestinyInventoryItemDefinition")
generatedEnums["PlugCategoryHashes"] = {}


def convertMixedStringToLeadingCapCamelCase(input: str) -> str:
    """
    :说明: `convertMixedStringToLeadingCapCamelCase`
    > 对于任何字符串，对特殊符号替换后将其转换为首字母大写的驼峰式命名

    :参数:
        * `input: str`: 输入字符串

    :返回:
        - `str`: 输出字符串
    """
    input = (
        input.replace(" ", "-")
        .replace(":", "-")
        .replace("/", "-")
        .replace(".", "-")
        .replace("_", "-")
        .replace("#", "-")
        .replace("：", "-")
    )
    return "".join(k.lower().capitalize() for k in input.split("-"))


for item in inventoryItems:
    # 对于每个项目，我们将尝试获取一个唯一的标签
    if (plug := item.get("plug")) and not item.get("redacted"):
        identifier = convertMixedStringToLeadingCapCamelCase(
            plug["plugCategoryIdentifier"]
        )
        # 如果我们已经生成了一个标签，我们将添加一个新的标签
        if identifier not in generatedEnums["PlugCategoryHashes"]:
            generatedEnums["PlugCategoryHashes"][identifier] = item["plug"][
                "plugCategoryHash"
            ]

allStats = getAll("DestinyStatDefinition")
allItemCategories = getAll("DestinyItemCategoryDefinition")
allSocketCategories = getAll("DestinySocketCategoryDefinition")
allBuckets = getAll("DestinyInventoryBucketDefinition")
allBreakers = getAll("DestinyBreakerTypeDefinition")

enumSources: List[Dict[str, Any]] = [
    {"name": "StatHashes", "data": allStats},
    {"name": "ItemCategoryHashes", "data": allItemCategories},
    {"name": "SocketCategoryHashes", "data": allSocketCategories},
    {"name": "BucketHashes", "data": allBuckets},
    {"name": "BreakerTypeHashes", "data": allBreakers},
]


# From 天阙：脚本解析顺序问题 这个函数要放在调用之前
# 这将寻找关于一个项目的额外信息，当它的displayProperties.name不是唯一时，就会包括在内
# 我试着让枚举参与其中，所以它们不太可能改变。
def tryToGetAdditionalStringContent(thing: dict) -> str:
    """
    :说明: `tryToGetAdditionalStringContent`
    > 尝试获取一个项目的唯一标识字符串

    :参数:
        * `thing: dict`: item 元数据

    :返回:
        - `str`: 生成的唯一标识
    """
    labels: List[str] = []

    # 对于 ItemCategories ，尝试使用它的类型作为标签
    if thing in allItemCategories:
        if grantDestinyItemType := thing.get("grantDestinyItemType"):
            labels.append(DestinyItemTypeLookup[grantDestinyItemType])
        if grantDestinySubType := thing.get("grantDestinySubType"):
            labels.append(DestinyItemSubTypeLookup[grantDestinySubType])

    # SocketCategories 处理
    if thing in allSocketCategories:
        if categoryStyle := thing.get("categoryStyle"):
            labels.append(DestinySocketCategoryStyleLookup[categoryStyle])

        # 或尝试查找具有此插口类型的示例项目，以显示有关此插口最终位置的更多信息
        # 目前这基本上有助于区分 Ship 插口和 Sparrow 插口
        exampleItems = [
            i
            for i in inventoryItems
            if (sockets := i.get("sockets"))
            and [
                j
                for j in sockets["socketCategories"]
                if j["socketCategoryHash"] == thing["hash"]
            ]
        ]

        if not exampleItems:
            labels.append("UNUSED")
        else:
            itemTypes = set(
                [
                    itemTypeDisplayName
                    for i in exampleItems
                    if (itemTypeDisplayName := i.get("itemTypeDisplayName"))
                ]
            )

            # 仅当所有找到的项目具有相同的项目类型时才使用此标签
            if len(itemTypes) == 1:
                labels.append(
                    convertMixedStringToLeadingCapCamelCase(list(itemTypes)[0])
                )

            traitIds = list(
                deduplicate(
                    [i.get("traitIds")[0] for i in exampleItems if i.get("traitIds")]
                )
            )

            if len(traitIds) == 1:
                labels.append(
                    convertMixedStringToLeadingCapCamelCase(traitIds[0].split(".")[-1])
                )

    # buckets 处理 ，尝试附加类型信息
    if thing in allBuckets:
        if category := thing.get("category"):
            labels.append(BucketCategoryLookup[category])

    if not labels:
        labels.append(f'{thing["hash"]}')

    labels = [""] + labels

    return "_".join(labels)


for i in enumSources:
    # 输出的数据在这里
    generatedEnums[i["name"]] = {}

    # 暂时记录我们见过的值与重复的值
    foundNames = set()
    dupeNames = set()

    for j in i["data"]:
        if (
            j.get("redacted")
            or not j["displayProperties"].get("name")
            or j["hash"] in ignoreHashes
        ):
            continue
        identifier = convertMixedStringToLeadingCapCamelCase(
            j["displayProperties"]["name"]
        )
        if identifier in foundNames:
            dupeNames.add(identifier)
        foundNames.add(identifier)

    # 在此处存储重复的命名项目
    dupeNamedItems = []

    # 这个循环用来构建输出的 enums
    for j in i["data"]:
        if (
            j.get("redacted")
            or not j["displayProperties"].get("name")
            or j["hash"] in ignoreHashes
        ):
            continue
        identifier = convertMixedStringToLeadingCapCamelCase(
            j["displayProperties"]["name"]
        )

        # 如果此枚举已经存在并且设置正确，则跳过
        if generatedEnums[i["name"]].get(identifier) == j["hash"]:
            continue

        # 如果它是一个预先确定的重复名称，以后再进行处理
        if identifier in dupeNames:
            dupeNamedItems.append(j)
            continue

        # 如果同名的东西指向不同的哈希值，那就是一个问题。
        # 我认为由于上述重复检查，这种情况不应该发生。
        if (
            generatedEnums[i["name"]].get(identifier)
            and generatedEnums[i["name"]].get(identifier) != j["hash"]
        ):
            logger.error(f'multiple {i["name"]} named {identifier}')
            continue

        # 如果运行到这里 那么存下它
        generatedEnums[i["name"]][identifier] = j["hash"]

    # 现在处理重复值
    deDupedIdentifiers = [
        convertMixedStringToLeadingCapCamelCase(
            dupeNamedItem["displayProperties"]["name"]
        )
        + tryToGetAdditionalStringContent(dupeNamedItem)
        for dupeNamedItem in dupeNamedItems
    ]

    # 如果生成的名字不都是唯一的，只能说是寄了
    if len(list(deduplicate(deDupedIdentifiers))) != len(deDupedIdentifiers):
        logger.error(
            f"couldn't properly make unique labels for {deDupedIdentifiers}, using hash"
        )
        continue

    # 如果我们到了这里，那么这些重复的东西都产生了不同的字符串
    for dupeNamedItem in dupeNamedItems:
        identifier = convertMixedStringToLeadingCapCamelCase(
            dupeNamedItem["displayProperties"]["name"]
        ) + tryToGetAdditionalStringContent(dupeNamedItem)

        generatedEnums[i["name"]][identifier] = dupeNamedItem["hash"]

# 枚举格式化输出
outString = "from enum import Enum\n\n"
for enumName, enumValues in generatedEnums.items():
    spaces = " " * 4
    outString += f"class {enumName}(int, Enum):\n{spaces}"
    outString += f"\n{spaces}".join(
        f"{label} = {value}" for label, value in enumValues.items()
    )
    outString += "\n\n"

writeFile("./output/generated_enums.py", outString)
logger.success("writeFile ./output/generated_enums.py")
writeFile("./data/generated_enums.py", outString)
logger.success("writeFile ./data/generated_enums.py")

logger.info("Generating Enums... Done")
