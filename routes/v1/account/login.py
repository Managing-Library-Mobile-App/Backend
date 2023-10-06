import datetime
from typing import Any

from flask_restful import reqparse  # type: ignore
from loguru import logger
from flasgger import swag_from
from flask_restful import Resource

from helpers.init import cache
from routes.v1.account.register import (
    contains_uppercase_char,
    contains_illegal_char,
    contains_special_char,
)


class InvalidLoginAttemptsCache(object):
    cache_table: str

    @staticmethod
    def _key(email) -> str:
        return f"invalid_login_attempt_{email}"

    @staticmethod
    def _value(lockout_timestamp, timestamps: list[int]) -> dict[str, list[int]]:
        return {
            "lockout_start": lockout_timestamp,
            "invalid_attempt_timestamps": timestamps,
        }

    @staticmethod
    def get(email) -> Any:
        try:
            key: str = InvalidLoginAttemptsCache._key(email)
            return cache.get(key)
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def delete(email) -> None:
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


class User:
    active: bool = False

    def __init__(self, username, password):
        self.username = username
        self.password = password


def authenticate_login_credentials(username, password) -> User | dict[str, str]:
    if contains_illegal_char(username):
        return {
            "user": None,
            "message": "username_illegal_chars",
            "details": "Illegal characters in username such as space",
        }
    if not contains_special_char(password):
        return {
            "user": None,
            "message": "password_no_special_chars",
            "details": "No special characters in password. Required at least one",
        }
    if contains_illegal_char(password):
        return {
            "user": None,
            "message": "password_illegal_chars",
            "details": "Illegal characters in password such as space",
        }
    if not contains_uppercase_char(password):
        return {
            "user": None,
            "message": "password_no_uppercase_char",
            "details": "Password has no uppercase letters. Required at least one.",
        }
    if len(username) < 10:
        return {
            "user": None,
            "message": "username_too_short",
            "details": "Minimum of 10 characters",
        }
    if len(username) > 50:
        return {
            "user": None,
            "message": "username_too_long",
            "details": "Max 50 characters",
        }
    if len(password) < 10:
        return {
            "user": None,
            "message": "password_too_short",
            "details": "Minimum of 10 characters",
        }
    if len(password) > 50:
        return {
            "user": None,
            "message": "password_too_long",
            "details": "Max 50 characters",
        }
    # TODO faktyczna weryfikacja użytkowników, którzy są w bazie
    user = User(username=username, password=password)
    if username == "Admin-1234" and password == "Admin-1234":
        # true: zalogowany, false: niezalogowany
        if user.active:
            return {
                "user": None,
                "message": "user_already_logged_in",
                "details": "User already logged in",
            }
        return {
            "user": user,
            "message": "password_too_long",
            "details": "Max 50 characters",
        }
    return {
        "user": None,
        "message": "authentication_failed",
        "details": "Wrong username or password",
    }


class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            location="json",
        )
        self.reqparse.add_argument("password", type=str, required=True, location="json")
        super(Login, self).__init__()

    @swag_from("login_swagger.yml")
    def get(self):
        args = self.reqparse.parse_args()
        username = args.get("username")
        password = args.get("password")
        login_output = authenticate_login(username, password)

        if login_output["user"] is not None:
            logger.info(f"Zarejestrowano użytkownika {login_output['user'].username}")
            return {"registered": True}
        logger.info(
            f"Nieudana próba logowania użytkownika. {login_output['message']}, {login_output['details']}"
        )
        return {
            "registered": False,
            "message": login_output["message"],
            "details": login_output["details"],
        }


def authenticate_login(username, password):
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    cache_results = InvalidLoginAttemptsCache.get(username)
    if cache_results and cache_results.get("lockout_start"):
        try:
            lockout_start = datetime.datetime.fromtimestamp(
                cache_results.get("lockout_start"), datetime.timezone.utc
            )
            locked_out = lockout_start >= (
                current_datetime + datetime.timedelta(minutes=-15)
            )
            if not locked_out:
                InvalidLoginAttemptsCache.delete(username)
            else:
                logger.warning(f"locked out user: {username}")
                return {
                    "user": None,
                    "message": "locked_user_login_attempts",
                    "details": "User locked because of too many unsuccessful attempts",
                }
        except Exception as e:
            logger.exception(e)
    login_data = authenticate_login_credentials(username=username, password=password)
    if login_data["user"] is not None:
        return {"user": login_data["user"]}
    InvalidLoginAttemptsCache.invalid_attempt(cache_results, current_datetime, username)
    return login_data
