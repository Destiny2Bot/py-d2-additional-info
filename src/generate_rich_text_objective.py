import re
from typing import List, Union

import ujson

from tools import writeFile, sortObject
from manifest import getAll, loadLocal

loadLocal()

objectives = getAll("DestinyObjectiveDefinition")
perks = getAll("DestinySandboxPerkDefinition")

iconFinder = r"(\[[^\]]+\]|[\uE000-\uF8FF])"

RichTextManifestSourceData = dict[str, List[Union[str, int]]]
richTexts: RichTextManifestSourceData = {}

for objective in objectives:
    match = re.findall(iconFinder, objective.get("progressDescription"))
    if match and len(match) == 1 and match[0] not in richTexts.keys():
        richTexts[match[0]] = ["Objective", objective["hash"]]

for perk in perks:
    match = re.findall(iconFinder, perk["displayProperties"].get("description", ""))
    if match and len(match) == 1 and match[0] not in richTexts.keys():
        richTexts[match[0]] = ["SandboxPerk", perk["hash"]]

# 输出时键包含了字符unicode信息(D2图标)，故有一些内容是不可视的
pretty = f"""# 输出时键包含了字符unicode信息(D2图标)，故有一些内容是不可视的
richTextManifestSourceData = {ujson.dumps(richTexts, ensure_ascii=False ,indent=4)}

richTextManifestExamples = richTextManifestSourceData
"""

writeFile("./output/objective_richTexts.py", pretty)
