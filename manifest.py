from typing import Any, Dict, Union

import ujson

from tools import readFile

BungieJSONFilePath = "./data/BungieManifest/BungieJSON.json"

manifest_json: Dict[Any, Any] = {}


def loadLocal() -> None:
    global manifest_json
    manifest_json = ujson.loads(readFile(BungieJSONFilePath))


def getAll(tablename: str = None) -> dict:
    if tablename:
        return manifest_json[tablename].values()
    return manifest_json


def get(tablename: str, hash: Union[str, int]) -> dict:
    return manifest_json[tablename].get(str(hash))
