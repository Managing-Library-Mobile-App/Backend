import flasgger
import flask
import flask_caching
import flask_jwt_extended
import flask_limiter
import flask_sqlalchemy
import werkzeug
from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_prometheus_metrics import register_metrics
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

load_dotenv()

app: flask.app.Flask = Flask(__name__)
limiter: flask_limiter.extension.Limiter = Limiter(
    get_remote_address,
    default_limits=["10000 per day", "5000 per hour"],
    storage_uri="memory://",
)
jwt: flask_jwt_extended.jwt_manager.JWTManager = JWTManager()
cache: flask_caching.Cache = Cache()
db: flask_sqlalchemy.extension.SQLAlchemy = SQLAlchemy()

# Prometheus metrics setup
register_metrics(app, app_version="v0.1.2", app_config="staging")
dispatcher: werkzeug.middleware.dispatcher.DispatcherMiddleware = DispatcherMiddleware(
    app.wsgi_app, {"/metrics": make_wsgi_app()}
)
