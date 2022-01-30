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


def getAll(tablename: str = None, language: str = "zh-chs") -> Union[dict, list]:
    if tablename:
        return list(manifest_json[language][tablename].values())
    return manifest_json


def get(
    tablename: str, hash: Union[str, int], itemname: str = None, language: str = "zh-chs"
) -> dict:
    if not hash and itemname:
        item = [
            item
            for item in manifest_json[language][tablename]
            if item.get("displayProperties")
            and item.get("displayProperties").get("name") == itemname
        ]
        return item[0] if item else {}
    else:
        return manifest_json[language][tablename].get(str(hash))
