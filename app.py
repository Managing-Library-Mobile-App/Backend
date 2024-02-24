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

from helpers.init import db, cache, jwt
from helpers.api_add_resources import api_add_resources_v1

from models.admin import Admin  # noqa
from models.author import Author  # noqa
from models.book import Book  # noqa
from models.book_announcement import BookAnnouncement  # noqa
from models.error import Error  # noqa
from models.library import Library  # noqa
from models.opinion import Opinion  # noqa
from models.user import User  # noqa

from data.test_data.fill_db_script import fill_db


app = Flask(__name__)
api = Api(app)
app.debug = True

host = os.environ.get("host")
port = os.environ.get("port")
database = os.environ.get("database")
user = os.environ.get("user")
password = os.environ.get("password")

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt.init_app(app)

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
    # Database setup
    with app.app_context():
        db.drop_all()
        db.create_all()
        fill_db(db)
    # App setup
    run_simple(
        hostname="0.0.0.0",
        port=5000,
        application=dispatcher,
        ssl_context=("static/cert.pem", "static/key.pem"),
    )
    application_start_date = datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S")
