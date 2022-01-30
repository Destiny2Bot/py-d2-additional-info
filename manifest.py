from typing import Any, Dict, Union

import ujson

from tools import readFile

BungieJSONFilePath = "./data/BungieManifest/"

manifest_json: Dict[str, Dict[Any, Any]] = {}


def loadLocal(language: str = "zh-chs") -> None:
    global manifest_json
    manifest_json[language] = ujson.loads(
        readFile(BungieJSONFilePath + f"BungieJSON_{language}.json")
    )


def getAll(tablename: str = None, language: str = "zh-chs") -> dict:
    if tablename:
        return manifest_json[language][tablename].values()
    return manifest_json


def get(tablename: str, hash: Union[str, int], language: str = "zh-chs") -> dict:
    return manifest_json[language][tablename].get(str(hash))
