import os

import requests

from log import logger

BungieJSONFilePath = "./data/BungieManifest/"


def getManifestOnline() -> dict:
    """
    :说明: `getManifestOnline`
    > 在线获取manifest信息

    :返回:
        - `dict`: Bungieapi返回值
    """
    url = "https://www.bungie.net/Platform/Destiny2/Manifest/"
    headers = {"X-API-KEY": "{}".format(os.environ.get("API_KEY"))}
    with requests.Session() as session:
        response = session.get(url=url, headers=headers)
        data = response.json()
    if data.get("ErrorCode") == 1 and data.get("Message") == "Ok":
        return data["Response"]
    else:
        raise


def downloadManifest(languages: list = ["zh-chs", "en"]) -> None:
    manifestInfo = getManifestOnline()
    version = manifestInfo["version"]
    logger.success(f"Manifest version: {version}")
    jsonWorldContentPaths = manifestInfo["jsonWorldContentPaths"]
    for language in languages:
        url = jsonWorldContentPaths[language]
        with requests.Session() as session:
            response = session.get(url="https://www.bungie.net" + url)
            data = response.content
        with open(BungieJSONFilePath + f"BungieJSON_{language}.json", "wb") as f:
            f.write(data)
            logger.success(f"Downloaded {language} manifest")

try:
    downloadManifest()
except Exception as e:
    print(e)
