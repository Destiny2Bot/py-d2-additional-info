from log import logger
from tools import copyFile

logger.info("Copying files... 拷贝文件")

copyFile("./data/legacy-triumphs.json", "./output/legacy-triumphs.json")
logger.success("copyFile ./data/legacy-triumphs.json -> ./output/legacy-triumphs.json")

copyFile("./data/stat_effects.py", "./output/stat_effects.py")
logger.success("copyFile ./data/stat_effects.py -> ./output/stat_effects.py")


# copyFile("./data/seasons/d2_season_info.py", "./output/d2_season_info.py") is in src/generate_season_info.py
logger.info("Copying files... Done")
