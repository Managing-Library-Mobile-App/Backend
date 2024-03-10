import datetime

from flask import make_response, jsonify
from flask_restful import Api
from werkzeug import run_simple

from helpers.api_add_resources import api_add_resources_v1
from helpers.init import db, app, dispatcher

from models.author import Author  # noqa
from models.book import Book  # noqa
from models.book_announcement import BookAnnouncement  # noqa
from models.library import Library  # noqa
from models.opinion import Opinion  # noqa
from models.user import User  # noqa

from data.test_data.fill_db_script import fill_db


api = Api(app)
api_add_resources_v1(api)

if __name__ == "__main__":
    # Database setup
    # TODO Delete later when delivering later versions
    with app.app_context():
        db.drop_all()
        db.create_all()
        fill_db(db)
        response = make_response(
            jsonify({"message": "All tokens have been revoked"}), 200
        )
    # App setup
    run_simple(
        hostname="0.0.0.0",
        port=5000,
        application=dispatcher,
        ssl_context=("static/cert.pem", "static/key.pem"),
        use_debugger=True,
    )
    # TODO Są dziwne problemy że jak odpalimy aplikację na 192...
    #  i potem na localhost to się sypie?
    application_start_date = datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S")
