from typing import Any, List, TypeVar, Callable, Hashable, Generator

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
