from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

# from loguru import logger
from dotenv import load_dotenv

load_dotenv()
cache = Cache()

# logger.add(
#     "database_and_logs/logs/logs.log",
#     format="Log: [{extra[log_id]}]: {time} | {level} | {message} ",
#     level="INFO",
#     enqueue=True,
# )


db: SQLAlchemy = SQLAlchemy()
