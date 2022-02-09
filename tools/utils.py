import re
from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Union,
    TypeVar,
    Callable,
    Hashable,
    Optional,
    Generator,
)

from log import logger

T = TypeVar("T")


def deduplicate(
    items: List[T],
    key: Callable[[T], Hashable] = None,
) -> Generator[T, None, None]:
    """
    :说明: `dedupelicate`
    > 去除列表中的重复项

    :参数:
        * `items: List[T]`: 列表

    :可选参数:
        * `key: Callable[[T], Hashable] = None`: 如果有Unhashable元素，使用此函数将其转为Hashable

    :生成:
        * `Generator[T, None, None]`: 去重后的列表
    """
    d = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in d:
            yield item
            d.add(val)


Sortable = TypeVar("Sortable", str, int)


def dedupeAndSortArray(
    items: List[Sortable], reverse: bool = False, key: Callable = None
) -> List[Sortable]:
    items = list(deduplicate(items))
    items.sort(reverse=reverse, key=key)
    return items


def diffArrays(all: List[T], exclude: Optional[List[T]] = None) -> List[T]:
    """
    :说明: `diffArrays`
    > [summary]

    :参数:
        * `all: List[T]`: [description]

    :可选参数:
        * `exclude: Optional[List[T]] = None`: [description]

    :返回:
        - `List[T]`: [description]
    """
    if exclude is None:
        return list(deduplicate(all))
    return [i for i in deduplicate(all) if i not in exclude]


def sortObject(o: dict[Sortable, Any]) -> dict[Sortable, Any]:
    """
    :说明: `sortObject`
    > 根据键值排序一个字典

    :参数:
        * `o: dict[Sortable, Any]`: 一个字典

    :返回:
        - `dict[Sortable, Any]`: 排序后的字典
    """
    _sorted: dict[Sortable, Any] = {}
    for k in sorted(o.keys()):
        _sorted[k] = o[k]
    return _sorted


def annotate(fileString: str, table: dict[int, str] = {}) -> str:
    """
    :说明: `annotate`
    > 对输出字符流添加注释

    :参数:
        * `fileString: str`: 无注释的字符流

    :可选参数:
        * `table: dict[int, str] = {}`: 用于查询注释的字典, 若为空则默认为道具表 `DestinyInventoryItemDefinition`

    :返回:
        - `str`: 添加注释后的字符流
    """
    import ujson

    from manifest import get

    from .file import readFile as readFile_utils

    translatDict: dict[str, dict[str, str]] = ujson.loads(
        readFile_utils("./data/sources/translate_dict.json")
    )
    translatDict_fields: dict[str, str] = translatDict["fields"]

    # 对 hash 值添加注释
    # 4+ 数字, 缩进, 以及可能被引号包围
    # 然后可能是逗号，然后可能是一些空格，然后是 EOL
    maybeHash = r"^( *)['\"]?(\d{2,})['\"]?(,?) *$"
    maybeEnKey = r"^( {4}| {12})['\"]?(\w+)['\"]?([: {,\[\]]*)$"
    retStrList = []
    for line in fileString.split("\n"):
        if findlist := re.findall(maybeHash, line):
            prefix, hash, suffix = findlist[0]
            if not (comment := table.get(int(hash))):
                if commentGet := get("DestinyInventoryItemDefinition", hash):
                    comment = commentGet.get("displayProperties", {"name": ""}).get(
                        "name"
                    )
            if not comment:
                comment = "未查询到的 hash"
                logger.warning(f"{hash} not found in table")
            comment = comment.replace("\n", " ")
            retStrList.append(f"{prefix}{hash}{suffix}  # {comment}")
        elif findlist := re.findall(maybeEnKey, line):
            prefix, field, suffix = findlist[0]
            comment = translatDict_fields.get(field, "未查询到的字段名")
            retStrList.append(f'{prefix}"{field}"{suffix}  # {comment}')
        else:
            retStrList.append(line)
    return "\n".join(retStrList)


if __name__ == "__main__":
    pass
