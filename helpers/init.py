from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from loguru import logger
from dotenv import load_dotenv

load_dotenv()
cache = Cache()

logger.add("database_and_logs/logs/logs.log", rotation="10000 seconds")

db: SQLAlchemy = SQLAlchemy()
