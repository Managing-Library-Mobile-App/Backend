import os

from flasgger import Swagger
from flask import Flask
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_prometheus_metrics import register_metrics
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

load_dotenv()

app = Flask(__name__)
api = Api()
limiter = Limiter(
    get_remote_address,
    default_limits=["10000 per day", "5000 per hour"],
    storage_uri="memory://",
)
jwt = JWTManager()
swagger = Swagger()
cache = Cache()
db: SQLAlchemy = SQLAlchemy()

host = os.environ.get("host")
port = os.environ.get("port")
database = os.environ.get("database")
user = os.environ.get("user")
password = os.environ.get("password")

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{user}:{password}@{host}:{port}/{database}"
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["CACHE_TYPE"] = "SimpleCache"

jwt.init_app(app)
cache.init_app(app)
db.init_app(app)
swagger.init_app(app)
limiter.init_app(app)

# Prometheus metrics setup
register_metrics(app, app_version="v0.1.2", app_config="staging")
dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
