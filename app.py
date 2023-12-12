import datetime
import os

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api
from helpers.init import db

from prometheus_client import make_wsgi_app
from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_prometheus_metrics import register_metrics

from helpers.api_add_resources import api_add_resources_v1
from helpers.init import cache
from flask_restful_swagger import swagger

app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion="1", api_spec_url="/api/v1/spec")
app.debug = True

host = os.environ.get("host")
database = os.environ.get("database")
user = os.environ.get("user")
password = os.environ.get("password")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{user}:{password}@{host}/{database}"
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
    port = int(os.environ.get("PORT", 5000))
    run_simple(
        hostname="0.0.0.0",
        port=5000,
        application=dispatcher,
        ssl_context=("static/cert.pem", "static/key.pem"),
    )
    application_start_date = datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S")
