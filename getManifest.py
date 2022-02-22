import requests

from log import logger
from manifest import getManifestOnline

BungieJSONFilePath = "./data/BungieManifest/"


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
