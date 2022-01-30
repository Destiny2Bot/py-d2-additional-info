import os, shutil
from typing import TypeVar, List
import numbers


T = TypeVar('T')

def deduplication(lst: List[T]) -> List[T]:
    return list(dict.fromkeys(lst))  

def copyFile(originPath: str, distPath: str):
    if os.path.exists(distPath):
        os.remove(distPath)
    else:
        if not os.path.exists(os.path.dirname(distPath)):
            os.makedirs(os.path.dirname(distPath))
    file = open(distPath, 'w', encoding='utf-8')
    file.close()
    shutil.copyfile(originPath, distPath)

def writeFile(path: str, content: str):
    file = open(path, 'w', encoding='utf-8')
    file.write(content)
    file.close()