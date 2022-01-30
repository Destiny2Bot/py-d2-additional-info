from tools.JsonIO import readjson
from typing import Union, List

BungieJSONFilePath = "./data/BungieManifest/BungieJSON.json"

manifest_json: dict

def loadLocal() -> None:
    global manifest_json
    manifest_json = readjson(BungieJSONFilePath)

def getAll(tablename: str = None) -> dict:
    if tablename:
        return manifest_json[tablename].values()
    return manifest_json

def get(tablename: str, hash: Union[str,int]) -> dict:
    return manifest_json[tablename].get(str(hash))