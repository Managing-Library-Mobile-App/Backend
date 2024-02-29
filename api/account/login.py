from __future__ import annotations

import datetime
import re
from typing import Any

from flask import jsonify, Response, make_response
from flask_jwt_extended import create_access_token
from loguru import logger
from flask_restful import Resource

from helpers.blocklist import BLOCK_LIST_USERS, BLOCK_LIST_TOKENS
from helpers.init import cache
from helpers.request_parser import RequestParser

from models.user import User


class InvalidLoginAttemptsCache(object):
    cache_table: str

    @staticmethod
    def _key(email: str) -> str:
        return f"invalid_login_attempt_{email}"

    @staticmethod
    def _value(
        lockout_timestamp: float, timestamps: list[float]
    ) -> dict[str, list[float] | float]:
        return {
            "lockout_start": lockout_timestamp,
            "invalid_attempt_timestamps": timestamps,
        }

    @staticmethod
    def get(email: str) -> Any:
        try:
            key: str = InvalidLoginAttemptsCache._key(email)
            return cache.get(key)
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def delete(email: str) -> None:
        try:
            cache.get()
            cache.delete(InvalidLoginAttemptsCache._key(email))
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def set(email, timebucket, lockout_timestamp=None) -> None:
        try:
            key: str = InvalidLoginAttemptsCache._key(email)
            value: dict = InvalidLoginAttemptsCache._value(
                lockout_timestamp, timebucket
            )
            cache.set(key, value)
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def invalid_attempt(cache_results, current_datetime, usr) -> str | None:
        invalid_attempt_timestamps = (
            cache_results["invalid_attempt_timestamps"] if cache_results else []
        )
        invalid_attempt_timestamps = [
            timestamp
            for timestamp in invalid_attempt_timestamps
            if timestamp
            > (current_datetime + datetime.timedelta(minutes=-15)).timestamp()
        ]
        invalid_attempt_timestamps.append(current_datetime.timestamp())
        if len(invalid_attempt_timestamps) >= 5:
            InvalidLoginAttemptsCache.set(
                usr, invalid_attempt_timestamps, current_datetime.timestamp()
            )
            return "locked_user_login_attempts"
        InvalidLoginAttemptsCache.set(usr, invalid_attempt_timestamps)
        return None


def authenticate_login_credentials(email, password) -> dict[str, str | None]:
    if not re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email):
        return {
            "message": "email_wrong_format",
            "details": "Wrong email format.",
        }
    if not re.fullmatch(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%*?&_-]{10,50}$",
        password,
    ):
        return {
            "message": "password_wrong_format",
            "details": """Wrong password format. Password should have from 10 to 50 characters.
            It should contain at least one upper letter, at least 1 lower letter, at least 1 number and
            at least one special character""",
        }

    user = None
    try:
        user = User.query.filter_by(email=email, password=password).first()
    except User.DoesNotExist:
        logger.info("User does not exist")
    if user:
        token = create_access_token(identity=email)
        BLOCK_LIST_USERS.add(email)
        BLOCK_LIST_TOKENS.add(token)
        return {
            "token": token,
            "message": "login_successful",
            "details": "Login successful",
        }
    return {
        "token": None,
        "message": "authentication_failed",
        "details": "Wrong email or password",
    }


class Login(Resource):
    def __init__(self) -> None:
        self.post_parser = RequestParser()
        self.post_parser.add_arg("email")
        self.post_parser.add_arg("password")
        super(Login, self).__init__()

    def post(self) -> Response:
        args = self.post_parser.parse_args()
        email = args.get("email")
        password = args.get("password")
        if email in BLOCK_LIST_USERS:
            logger.info(BLOCK_LIST_USERS)
            logger.info(email)
            return make_response(
                jsonify(
                    password_changed=False,
                    message="user_already_logged_in",
                    details="User already logged in",
                ),
                401,
            )
        login_output = authenticate_login(email, password)

        if login_output["message"] == "login_successful":
            logger.info(f"Zalogowano użytkownika {email}")
            return make_response(
                jsonify(
                    logged_in=True,
                    token=login_output["token"],
                    message=login_output["message"],
                    details=login_output["details"],
                ),
                200,
            )
        logger.info(
            f"Nieudana próba logowania użytkownika. {login_output['message']}, {login_output['details']}"
        )
        if isinstance(login_output["message"], str) and isinstance(
            login_output["details"], str
        ):
            return make_response(
                jsonify(
                    registered=False,
                    message=login_output["message"],
                    details=login_output["details"],
                ),
                401,
            )
        raise Exception("Unexpected login behavior! Raised exception!")


def authenticate_login(email, password) -> dict[str, str | None]:
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    cache_results = InvalidLoginAttemptsCache.get(email)
    if cache_results and cache_results.get("lockout_start"):
        try:
            lockout_start = datetime.datetime.fromtimestamp(
                cache_results.get("lockout_start"), datetime.timezone.utc
            )
            locked_out = lockout_start >= (
                current_datetime + datetime.timedelta(minutes=-15)
            )
            if not locked_out:
                InvalidLoginAttemptsCache.delete(email)
            else:
                logger.warning(f"locked out user: {email}")
                return {
                    "user": None,
                    "message": "locked_user_login_attempts",
                    "details": "User locked because of too many unsuccessful attempts",
                }
        except Exception as e:
            logger.exception(e)
    login_data = authenticate_login_credentials(email=email, password=password)
    InvalidLoginAttemptsCache.invalid_attempt(cache_results, current_datetime, email)
    return login_data
