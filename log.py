import sys

from loguru import logger

from config import config

logger.remove()

handler = logger.add(sys.stderr, level=config.log_level)
