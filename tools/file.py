import os
import shutil
from typing import Dict, Union
from pathlib import Path

import ujson


def copyFile(src: str, dst: str):
    """
    :说明: `copyFile`
    > 复制文件

    :参数:
      * `src: str`: 原文件路径
      * `dst: str`: 目标路径 为文件夹则保留原文件名置于该文件夹下
    """
    if os.path.exists(dst):
        os.remove(dst)
    else:
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
    shutil.copy2(src, dst)


def writeFile(path: Union[str, Path], content: Union[str, Dict]):
    """
    :说明: `writeFile`
    > 将数据写入文件

    :参数:
      * `path: Union[str, Path]`: 目标文件路径
      * `content: Union[str, Dict]`: 写入内容
    """
    with open(path, "w", encoding="utf-8") as file:
        if isinstance(content, dict):
            ujson.dump(content, file, ensure_ascii=False, indent=4)
        else:
            file.write(content)


def readFile(path: Union[str, Path]) -> str:
    """
    :说明: `readFile`
    > 读取文件内容

    :参数:
      * `path: Union[str, Path]`: 文件路径

    :返回:
      - `str`: 文件内容
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
