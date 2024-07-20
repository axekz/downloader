from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, format="{time:HH:mm:ss} | {level} | {message}", colorize=True, level="INFO")
