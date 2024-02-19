import datetime
import os

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api

from prometheus_client import make_wsgi_app
from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_prometheus_metrics import register_metrics

from helpers.init import db
from helpers.api_add_resources import api_add_resources_v1
from helpers.init import cache

from models.admin import Admin
from models.author import Author
from models.book import Book
from models.book_announcement import BookAnnouncement
from models.error import Error
from models.library import Library
from models.opinion import Opinion
from models.user import User

from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)
app.debug = True

host = os.environ.get("host")
host_alternative = os.environ.get("host_alternative")
port = os.environ.get("port")
database = os.environ.get("database")
user = os.environ.get("user")
password = os.environ.get("password")

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{user}:{password}@{host}:{port}/{database}"
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["CACHE_TYPE"] = "SimpleCache"
cache.init_app(app)

db.init_app(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10000 per day", "5000 per hour"],
    storage_uri="memory://",
)

# Prometheus metrics setup
register_metrics(app, app_version="v0.1.2", app_config="staging")
dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

api_add_resources_v1(api)

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
    run_simple(
        hostname="0.0.0.0",
        port=5000,
        application=dispatcher,
        ssl_context=("static/cert.pem", "static/key.pem"),
    )
    application_start_date = datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S")
