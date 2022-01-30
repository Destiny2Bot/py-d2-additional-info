from typing import Dict, List, Union

from tools import writeFile
from manifest import getAll, loadLocal
from data.generated_enums import ItemCategoryHashes

loadLocal()

inventoryItems = getAll("DestinyInventoryItemDefinition")


class Telemetry:
    arc: bool = False
    void: bool = False
    solar: bool = False

    def to_dict(self) -> dict:
        return {
            "arc": self.arc,
            "void": self.void,
            "solar": self.solar,
        }


class GhostType:
    xp: bool = False
    resource: bool = False
    cache: bool = False
    scanner: bool = False
    glimmer: bool = False
    telemetry: Telemetry = Telemetry()
    improved: bool = False

    def to_dict(self) -> dict:
        return {
            "xp": self.xp,
            "resource": self.resource,
            "cache": self.cache,
            "scanner": self.scanner,
            "glimmer": self.glimmer,
            "telemetry": self.telemetry.to_dict(),
            "improved": self.improved,
        }


class GhostData:
    location: Union[str, bool]
    type: GhostType

    def to_dict(self) -> dict:
        return {
            "location": self.location,
            "type": self.type.to_dict(),
        }


def getLocation(description: str) -> Union[str, bool]:
    lcDescription = description.lower()
    # print(lcDescription)
    if "欧洲无人区" in lcDescription:
        return "欧洲无人区"
    elif "土卫六" in lcDescription:
        return "土卫六"
    elif "涅索斯" in lcDescription:
        return "涅索斯"
    elif "木卫一" in lcDescription:
        return "木卫一"
    elif "水星" in lcDescription:
        return "水星"
    elif "赫拉斯盆地" in lcDescription:
        return "赫拉斯盆地"
    elif "纷争海岸" in lcDescription:
        return "纷争海岸"
    elif "幽梦之城" in lcDescription:
        return "幽梦之城"
    elif "打击" in lcDescription:
        return "打击"
    elif "熔炉竞技场" in lcDescription:
        return "熔炉竞技场"
    elif "智谋" in lcDescription:
        return "智谋"
    elif "利维坦" in lcDescription:
        return "利维坦"
    elif "月球" in lcDescription:
        return "月球"
    else:
        return False


def getImporved(description: str, name: str) -> bool:
    if "增强版" in name or "以更快的速度" in description:
        return True
    return False


def getType(description: str, name: str) -> GhostType:
    ghostType = GhostType()
    ghostType.improved = getImporved(description, name)
    if "经验" in description:
        ghostType.xp = True
    if "缓存箱" in description:
        ghostType.cache = True
    if "资源" in description:
        ghostType.resource = True
    if "获得额外" in description:
        ghostType.scanner = True
    if "微光" in description:
        ghostType.glimmer = True

    if "生成枪匠遥测数据" in description:
        if "电弧武器击杀" in description:
            ghostType.telemetry.arc = True
        elif "虚空武器击杀" in description:
            ghostType.telemetry.void = True
        elif "烈日武器击杀" in description:
            ghostType.telemetry.solar = True
        elif "任意元素武器击杀" in description:
            ghostType.telemetry.arc = True
            ghostType.telemetry.void = True
            ghostType.telemetry.solar = True

    return ghostType


ghostPerks: Dict[str, dict] = {}

# 随机模组
ghostPerkHashDenyList = [2328497849]

for item in inventoryItems:
    ghostData = GhostData()
    hash: int = item["hash"]
    description: str = item["displayProperties"]["description"]
    name: str = item["displayProperties"]["name"]
    categoryHashes: List[int] = item.get("itemCategoryHashes", [])
    if (ItemCategoryHashes.机灵模组特性 in categoryHashes) and (
        hash not in ghostPerkHashDenyList
    ):
        ghostData.location = getLocation(description)
        ghostData.type = getType(description.lower(), name.lower())
    else:
        continue
    # print(ghostData.location)
    ghostPerks[str(hash)] = ghostData.to_dict()

writeFile("./output/ghost-perks.json", ghostPerks)
