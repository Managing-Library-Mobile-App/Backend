from flask_caching import Cache
from loguru import logger

cache = Cache()

logger.add("database_and_logs/logs/logs.log", rotation="10000 seconds")
