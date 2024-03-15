import datetime

from flasgger import Swagger
from flask_restful import Api
from werkzeug import run_simple

import env
from helpers.api_add_resources import api_add_resources
from helpers.init import db, app, dispatcher, jwt, cache, limiter

from models.author import Author  # noqa
from models.book import Book  # noqa
from models.book_announcement import BookAnnouncement  # noqa
from models.library import Library  # noqa
from models.opinion import Opinion  # noqa
from models.user import User  # noqa

from data.test_data.fill_db_script import fill_db

SWAGGER_TEMPLATE = {
    "securityDefinitions": {
        "APIKeyHeader": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}
swagger = Swagger(app, template=SWAGGER_TEMPLATE)
api = Api(app)
api_add_resources(api)

app.config["JWT_SECRET_KEY"] = env.JWT_SECRET_KEY

host = env.host
port = env.port
database = env.database
user = env.user
password = env.password

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{user}:{password}@{host}:{port}/{database}"
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["CACHE_TYPE"] = "SimpleCache"


# app.config["PROPAGATE_EXCEPTIONS"] = True


jwt.init_app(app)
cache.init_app(app)
db.init_app(app)
limiter.init_app(app)

if __name__ == "__main__":
    # Database setup
    # TODO Delete later when delivering later versions
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
    # TODO Są dziwne problemy że jak odpalimy aplikację na 192...
    #  i potem na localhost to się sypie?
    application_start_date = datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S")
