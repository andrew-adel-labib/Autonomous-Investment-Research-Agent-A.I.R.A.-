import sys
from loguru import logger

logger.remove()

logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    colorize=True
)

logger.add(
    "logs/aira.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="DEBUG",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

def get_logger():
    return logger