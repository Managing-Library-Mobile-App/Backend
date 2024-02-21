from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
cache = Cache()
db: SQLAlchemy = SQLAlchemy()

jwt = JWTManager()
