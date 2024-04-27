import datetime
import os

import argparse

import flask_restful
from flask_restful import Api
from loguru import logger
from werkzeug import run_simple

from test_data.fill_db_script import fill_db
from helpers.api_add_resources import api_add_resources
from helpers.init import app, cache, db, dispatcher, jwt, limiter
from models.author import Author  # noqa
from models.book import Book  # noqa
from models.library import Library  # noqa
from models.opinion import Opinion  # noqa
from models.user import User  # noqa

api: flask_restful.Api = Api(app)
api_add_resources(api)

parser = argparse.ArgumentParser(description="Description of your script")
parser.add_argument(
    "type_of_db",
    type=str,
    help="Type of db. Currently used: 'api_tests' or 'e2e_tests' or 'prod'",
)
args = parser.parse_args()

host: str = os.environ.get("host")
port: str = os.environ.get("port")
database: str = args.type_of_db
user: str = os.environ.get("user")
password: str = os.environ.get("password")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{user}:{password}@{host}:{port}/{database}"
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["BUNDLE_ERRORS"] = True


jwt.init_app(app)
cache.init_app(app)
db.init_app(app)
limiter.init_app(app)

if __name__ == "__main__":
    import psycopg2

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port,
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {database}")
        logger.info(f"CREATED DATABASE {database}")
        cur.close()
        conn.close()
    except psycopg2.errors.DuplicateDatabase:
        pass
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
