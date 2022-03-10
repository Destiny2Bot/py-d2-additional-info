# 为可制造武器收集增强的内在特性，以便我们可以正确处理它们的奖励统计数据。

from typing import List

import ujson

from log import logger
from tools import annotate, writeFile
from manifest import get, getAll, loadLocal
from data.generated_enums import PlugCategoryHashes

logger.info("Generating Crafting Enhance Intrinsics... 可制作武器的内在特性")

loadLocal()
allEnhancedIntrinsics: List[int] = []

inventoryItems = getAll("DestinyInventoryItemDefinition")

for pattern in (i for i in inventoryItems if i.get("crafting")):
    if sockets := pattern.get("sockets"):
        frameSocket = [
            s
            for s in sockets["socketEntries"]
            if (
                socketTypeHash := get("DestinySocketTypeDefinition", s["socketTypeHash"])
            )
            and any(
                [
                    j["categoryHash"] == PlugCategoryHashes.Intrinsics
                    for j in socketTypeHash["plugWhitelist"]
                ]
            )
        ]
        if frameSocket and frameSocket[0].get("reusablePlugSetHash"):
            plugSet = get(
                "DestinyPlugSetDefinition", frameSocket[0]["reusablePlugSetHash"]
            )
            if reusablePlugItems := plugSet.get("reusablePlugItems"):
                enhancedIntrinsics = [
                    p["plugItemHash"]
                    for p in reusablePlugItems
                    if (
                        plugItem := get(
                            "DestinyInventoryItemDefinition", p["plugItemHash"]
                        )
                    )
                    and any(
                        [
                            j.get("isConditionallyActive")
                            for j in plugItem["investmentStats"]
                        ]
                    )
                ]
                if enhancedIntrinsics:
                    allEnhancedIntrinsics.extend(enhancedIntrinsics)
pretty = f"""enhancedIntrinsics = set({ujson.dumps(allEnhancedIntrinsics, ensure_ascii=False, indent=4)})"""

annotated = annotate(pretty)
writeFile("./output/crafting_enhanced_intrinsics.py", annotated)
logger.success("wirteFile: ./output/crafting_enhanced_intrinsics.py")
