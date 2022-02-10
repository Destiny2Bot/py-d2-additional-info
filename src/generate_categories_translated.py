from typing import List, Union, Optional

import ujson
from pydantic import BaseModel, validator

from log import logger
from tools import readFile, writeFile, deduplicate
from manifest import get, getAll, loadLocal


def _translater_for_table(
    item: str,
    keyName: str,
    enDict: list,
    tableName: str = "DestinyInventoryItemDefinition",
) -> str:
    """
    :说明: `_translater_for_table`
    > 需要查数据表的基础验证器，通过 `enDict` 和 `tableName` 参数查找对应的中文名

    :参数:
      * `item: str`: 需要翻译的名称
      * `keyName: str`: 翻译字典的类别
      * `enDict: list`: 原语言manifest中对应的表

    :可选参数:
      * `tableName: str = 'DestinyInventoryItemDefinition'`: 表名

    :返回:
        - `str`: 翻译后的名称，若翻译失败则返回原名
    """ """"""
    if unKnownItems.get(keyName) is None:
        unKnownItems[keyName] = []

    # 如果是数字则跳过
    if item.isdigit():
        logger.debug(f"{keyName.upper()}\t|\t[{item}] \t is digit \t continue")
        return item

    # 尝试在翻译表中查找
    itemName = translatDict.get(keyName, {}).get(item)
    if itemName:
        pass
    else:
        # 从英文库中获取
        itemInfo = [i for i in enDict if i["displayProperties"]["name"] == item]
        if not itemInfo:
            if item not in unKnownItems[keyName]:
                unKnownItems[keyName].append(item)
            logger.warning(
                f"{keyName.upper()}\t|\t[{item}] \t not found in {tableName}[en]"
            )
            return item

        itemName = (
            get(tableName, itemInfo[0].get("hash"))
            .get("displayProperties", {"name": ""})
            .get("name")
        )
    if itemName:
        logger.debug(f"{keyName.upper()}\t|\t[{item}] \t translated to \t [{itemName}]")

        if item not in translatDict["items"].keys():
            translatDict["items"][item] = itemName
        return itemName
    else:
        logger.warning(
            f"{keyName.upper()}\t|\t[{itemName}] \t not found in {tableName}[zh-chs]"
        )
        return item


def itemsTranslater(items: List[str]) -> List[str]:
    """
    :说明: `itemsTranslater`
    > 将 item 英文名译为中文，来源为翻译表中 `items` 字段与 `manifest[InventoryItems]` 表项

    :参数:
      * `items: List[str]`: 需要翻译的名称列表

    :返回:
        - `List[str]`: 翻译后的名称, 若翻译失败则返回原名
    """
    itemNames = []
    itemNameList = [
        _translater_for_table(item, keyName="items", enDict=list(allInventoryItems_en))
        for item in items
    ]
    for itemName in itemNameList:
        itemNames.extend(itemName.split("||##||"))
    return list(deduplicate(itemNames))


def sourcesTranslater(sourcesNames: List[str]) -> List[str]:
    """
    :说明: `sourcesTranslater`
    > 将 includes 中文名译为英文, ，来源为翻译表中 `sources` 字段与 `manifest[Collectibles]` 表项

    :参数:
      * `sourcesNames: List[str]`: 需要翻译的名称列表

    :返回:
        - `List[str]`: 翻译后的名称, 若翻译失败则返回原名
    """
    sourcesNamesCn = []
    for sourceName in sourcesNames:
        # 如果是数字则跳过
        if sourceName.isdigit():
            logger.debug(f"SCOURCE\t|\t[{sourceName}] \t is digit \t continue")
            sourcesNamesCn.append(sourceName)
            continue

        # 尝试在翻译表中查找
        sourceNameCn = translatDict["sources"].get(sourceName)
        if sourceNameCn:
            pass
        else:
            # 从英文库中获取
            collectibleItemInfo = [
                i for i in allCollectibles_en if i["sourceString"] == sourceName
            ]
            if not collectibleItemInfo:
                # 对未查询到的内容获取参考文本
                tips = ""
                if sourceName not in unKnownItems["sources"]:
                    tipCollectibleItems = [
                        i for i in allCollectibles_en if sourceName in i["sourceString"]
                    ][:3]
                    tips = f'\nrefer to:\n\t"{sourceName}": "",\n\t' + "\n\t".join(
                        get("DestinyCollectibleDefinition", i["hash"])["sourceString"]
                        for i in tipCollectibleItems
                    )
                    unKnownItems["sources"].append(sourceName)
                logger.warning(
                    f"SCOURCE\t|\t[{sourceName}] \t not found in DestinyCollectibleDefinition[en]"
                    + tips
                )
                sourcesNamesCn.append(sourceName)
                continue

            sourceNameCn = get(
                "DestinyCollectibleDefinition", collectibleItemInfo[0].get("hash")
            ).get("sourceString")
        if sourceNameCn:
            logger.debug(
                f"SCOURCE\t|\t[{sourceName}] \t translated to \t [{sourceNameCn}]"
            )
            sourcesNamesCn.extend(sourceNameCn.split("||##||"))
            if sourceName not in translatDict["sources"].keys():
                translatDict["sources"][sourceName] = sourceNameCn
        else:
            logger.warning(
                f"SCOURCE\t|\t[{sourceName}] \t not found in DestinyCollectibleDefinition[zh-chs]"
            )
            sourcesNamesCn.append(sourceName)
    return list(deduplicate(sourcesNamesCn))


def presentationNodesTranslater(presentations: List[str]) -> List[str]:
    """
    :说明: `presentationNodesTranslater`
    > 将 presentationNodes 中文名译为英文, ，来源为 `manifest[presentationNodes]` 表项

    :参数:
      * `sourcesNames: List[str]`: 需要翻译的名称列表

    :返回:
        - `List[str]`: 翻译后的名称, 若翻译失败则返回原名
    """
    presentationNodes = []
    unKnownItems["presentationNodes"] = []
    presentationNameList = [
        _translater_for_table(
            presentation,
            keyName="presentationNodes",
            enDict=list(allPresentationNodes_en),
            tableName="DestinyPresentationNodeDefinition",
        )
        for presentation in presentations
    ]
    for presentationName in presentationNameList:
        presentationNodes.extend(presentationName.split("||##||"))
    return list(deduplicate(presentationNodes))


def _translater(originStrs: str, keyName: str) -> str:
    """
    :说明: `_translater`
    > 仅需查询字典的基础验证器函数

    :参数:
        * `originStrs: str`: 需要翻译的字符串
        * `keyName: str`: 翻译表的字段名 key

    :返回:
        - `str`: 翻译后的字符串，若翻译失败则返回原字符串
    """
    retName = translatDict[keyName].get(originStrs)
    if unKnownItems.get(keyName) is None:
        unKnownItems[keyName] = []
    if retName:
        logger.debug(
            f"{keyName.upper()}\t|\t[{originStrs}] \t translated to \t [{retName}]"
        )
    else:
        if originStrs not in unKnownItems[keyName]:
            unKnownItems[keyName].append(originStrs)
        logger.warning(
            f"{keyName.upper()}\t|\t[{originStrs}] \t not found in TranslateDict"
        )
    return retName or originStrs


def fieldsTranslater(originStrs: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    :说明: `fieldsTranslater`
    > `fields` 字段验证函数，主要为分类简称和别名，不一定与游戏原名称相同，一般为游戏原名称子集

    :参数:
        * `originStrs: Union[str, List[str]]`: 需要翻译的字符串或字符串列表

    :返回:
        - `Union[str, List[str]]`: 返回翻译后的内容，若翻译失败则返回原字符串
    """
    if isinstance(originStrs, str):
        return _translater(originStrs, "fields")
    elif isinstance(originStrs, list):
        return [_translater(i, "fields") for i in originStrs]
    else:
        return originStrs


class CategoriesSources(BaseModel):
    """
    :说明: `CategoriesSources`
    > 对来源信息的筛选设定
    """

    includes: List[str]
    """字符串列表， 如果一个来源描述包含其中之一，它可能指的是这个 sourceTag"""

    excludes: Optional[List[str]]
    """字符串列表，如果一个来源描述包含其中之一, 他不可能指这个 sourceTag"""

    items: Optional[List[Union[str, int]]]
    """一个包含来源英文名或来源 hash 的列表"""

    alias: Optional[str]
    """将此类别复制到另一个 sourceTag"""

    presentationNodes: Optional[List[Union[str, int]]]
    """
    presentationNodes 包含一个 items (Collections) 的集合,
    我们将通过名称或哈希找到 presentationNodes 并将他们的子项目添加到 来源中
    """

    searchString: Optional[List[str]]

    _includesValidator = validator("includes", pre=True, allow_reuse=True)(
        sourcesTranslater
    )

    _excludesValidator = validator("excludes", pre=True, allow_reuse=True)(
        sourcesTranslater
    )

    _itemsValidator = validator("items", pre=True, allow_reuse=True)(itemsTranslater)

    _aliasValidator = validator("alias", pre=True, allow_reuse=True)(fieldsTranslater)

    _presentationNodesValidator = validator(
        "presentationNodes", pre=True, allow_reuse=True
    )(presentationNodesTranslater)

    _searchStringValidator = validator("searchString", pre=True, allow_reuse=True)(
        fieldsTranslater
    )


class Categories(BaseModel):
    """
    :说明: `Categories`
    > 来源类别数据类
    """

    sources: dict[
        str,  # 一个 sourceTag, i.e. "adventures" or "deadorbit" or "zavala" or "crucible"
        CategoriesSources,
    ]

    exceptions: List[List[str]]

    @validator("sources", pre=True)
    def sourcesKeyTranslater(cls, sources):
        return {fieldsTranslater(k): v for k, v in sources.items()}

    @validator("exceptions", pre=True)
    def exceptionsStrTranslater(cls, sources):
        return [[hash, *sourcesTranslater([str])] for hash, str in sources]


# 加载中英文数据表信息
loadLocal()
loadLocal(language="en")

allInventoryItems = getAll("DestinyInventoryItemDefinition")
allInventoryItems_en = getAll("DestinyInventoryItemDefinition", language="en")
allCollectibles = getAll("DestinyCollectibleDefinition")
allCollectibles_en = getAll("DestinyCollectibleDefinition", language="en")
allPresentationNodes = getAll("DestinyPresentationNodeDefinition")
allPresentationNodes_en = getAll("DestinyPresentationNodeDefinition", language="en")

# 妈的这俩必须定义 要不写个类吧
unKnownItems: dict[str, List[str]] = {}
translatDict: dict[str, dict[str, str]] = ujson.loads(
    readFile("./data/sources/translate_dict.json")
)


categories = Categories.parse_file("./data/sources/categories.json")


for k, v in unKnownItems.items():
    if v:
        logger.warning(
            f"{k}\t{len(v)} not translate\n\t"
            + "\n\t".join(f'"{i}": "",' for i in v)
            + "\n"
        )
    else:
        logger.success(f"{k.upper()} all translate")

writeFile("./data/sources/translate_dict.json", translatDict)

writeFile(
    "./data/sources/categories_translated.json", categories.dict(exclude_none=True)
)
