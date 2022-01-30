from loguru import logger
from config import config

logger.level(config.log_level)