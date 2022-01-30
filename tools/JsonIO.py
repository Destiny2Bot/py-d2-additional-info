import os, ujson, aiofiles, shutil

async def readjson_async(filePath: str) -> dict[str, dict]:
    if not os.path.exists(filePath):
        raise
    async with aiofiles.open(filePath, 'r', encoding='utf-8') as f:
        content = await f.read()
    content = ujson.loads(content)
    return content

def readjson(filePath: str) -> dict:
    if not os.path.exists(filePath):
        raise
    with open(filePath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = ujson.loads(content)
    return content

async def writejson_async(filePath: str, data: dict) -> bool:
    if not os.path.exists(os.path.dirname(filePath)):
        os.makedirs(os.path.dirname(filePath))
    async with aiofiles.open(filePath, 'w', encoding='utf-8') as f:
        await f.write(ujson.dumps(data, ensure_ascii=False, indent=4))
    return True

def writejson(filePath: str, data: dict) -> bool:
    if not os.path.exists(os.path.dirname(filePath)):
        os.makedirs(os.path.dirname(filePath))
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(ujson.dumps(data, ensure_ascii=False, indent=4))
    return True