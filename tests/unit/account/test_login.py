import os
import sys
from os import path

from api.account.login import authenticate_login_credentials
from helpers.blocklist import LOGGED_IN_USER_TOKENS
from test_data.fill_db_script import create_admin_accounts_in_db

sys.path.append(path.join(path.dirname(__file__), "...."))

from flask import Flask
import unittest

from helpers.init import db, jwt, cache, limiter

import datetime
from helpers.request_response import create_response
from static.responses import (
    USER_NOT_LOGGED_IN_RESPONSE,
    PASSWORD_WRONG_FORMAT_RESPONSE,
    EMAIL_WRONG_FORMAT_RESPONSE,
    ALREADY_LOGGED_IN_RESPONSE,
    LOGIN_SUCCESSFUL_RESPONSE,
)


class AppDbTests(unittest.TestCase):
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        host: str = os.environ.get("host")
        port: str = os.environ.get("port")
        database: str = "test"
        user: str = os.environ.get("user")
        password: str = os.environ.get("password")

        self.app = Flask(__name__)

        self.app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.app.config["SECRET_KEY"] = "SECRET_KEY"
        self.app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
        self.app.config["CACHE_TYPE"] = "SimpleCache"
        self.app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
        self.app.config["BUNDLE_ERRORS"] = True
        jwt.init_app(self.app)
        cache.init_app(self.app)
        limiter.init_app(self.app)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            create_admin_accounts_in_db(db)

    def test_positive_login_user_validation_correct_credentials_admin(self):
        with self.app.app_context():
            authentication_json = authenticate_login_credentials(
                email="adminadmin@gmail.com",
                password="AdminAdmin-1234",
                language="",
                cache_results=None,
                current_datetime=datetime.datetime.now(),
            ).json
            assert (
                authentication_json
                == create_response(
                    LOGIN_SUCCESSFUL_RESPONSE,
                    {"token": authentication_json["token"]},
                    language="",
                    not_translated={"token"},
                ).json
            )

    def test_negative_login_user_validation_contains_illegal_char_email(self):
        with self.app.app_context():
            authentication_json = authenticate_login_credentials(
                email="admina$dmin@gmail.com",
                password="AdminAdmin-1234",
                language="",
                cache_results=None,
                current_datetime=datetime.datetime.now(),
            ).json
            assert (
                authentication_json
                == create_response(EMAIL_WRONG_FORMAT_RESPONSE, language="").json
            )

    def test_negative_login_user_validation_not_contains_special_char_password(self):
        with self.app.app_context():
            authentication_json = authenticate_login_credentials(
                email="adminadmin@gmail.com",
                password="AdminAdmin1234",
                language="",
                cache_results=None,
                current_datetime=datetime.datetime.now(),
            ).json
            assert (
                authentication_json
                == create_response(PASSWORD_WRONG_FORMAT_RESPONSE, language="").json
            )

    def test_negative_login_user_validation_not_contains_uppercase_char_password(self):
        with self.app.app_context():
            authentication_json = authenticate_login_credentials(
                email="adminadmin@gmail.com",
                password="adminadmin-1234",
                language="",
                cache_results=None,
                current_datetime=datetime.datetime.now(),
            ).json
            assert (
                authentication_json
                == create_response(PASSWORD_WRONG_FORMAT_RESPONSE, language="").json
            )

    def test_negative_login_user_validation_wrong_username_or_password(self):
        with self.app.app_context():
            authentication_json = authenticate_login_credentials(
                email="email@email.com",
                password="Password-123",
                language="",
                cache_results=None,
                current_datetime=datetime.datetime.now(),
            ).json
            assert (
                authentication_json
                == create_response(USER_NOT_LOGGED_IN_RESPONSE, language="").json
            )

    def test_negative_login_user_validation_already_logged_in(self):
        with self.app.app_context():
            authenticate_login_credentials(
                email="adminadmin@gmail.com",
                password="AdminAdmin-1234",
                language="",
                cache_results=None,
                current_datetime=datetime.datetime.now(),
            )
            authentication_json = authenticate_login_credentials(
                email="adminadmin@gmail.com",
                password="AdminAdmin-1234",
                language="",
                cache_results=None,
                current_datetime=datetime.datetime.now(),
            ).json
            assert (
                authentication_json
                == create_response(
                    ALREADY_LOGGED_IN_RESPONSE,
                    {"token": LOGGED_IN_USER_TOKENS["adminadmin@gmail.com"]},
                    language="",
                    not_translated={"token"},
                ).json
            )
