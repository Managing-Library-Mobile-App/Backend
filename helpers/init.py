from flask_caching import Cache
from loguru import logger
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import time

load_dotenv()
cache = Cache()

logger.add("database_and_logs/logs/logs.log", rotation="10000 seconds")

while True:
    try:
        host = os.environ.get("host")
        database = os.environ.get("database")
        user = os.environ.get("user")
        password = os.environ.get("password")
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        logger.info("Database connection successful.")
        break
    except Exception as err:
        logger.error("Connecting to database failed. Error message: %s", err)
        time.sleep(5)
