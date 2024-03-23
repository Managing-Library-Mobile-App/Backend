import datetime
import re
from typing import Any

from flask import Response
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from loguru import logger

from helpers.blocklist import LOGGED_IN_USER_TOKENS
from helpers.init import cache
from helpers.request_parser import RequestParser
from models.user import User
from static.responses import USER_NOT_LOGGED_IN_RESPONSE, create_response, LOCKED_USER_LOGIN_ATTEMPTS_RESPONSE, \
    PASSWORD_WRONG_FORMAT_RESPONSE, EMAIL_WRONG_FORMAT_RESPONSE, ALREADY_LOGGED_IN_RESPONSE, LOGIN_SUCCESSFUL_RESPONSE


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
        key: str = InvalidLoginAttemptsCache._key(email)
        return cache.get(key)

    @staticmethod
    def delete(email: str) -> None:
        cache.get()
        cache.delete(InvalidLoginAttemptsCache._key(email))

    @staticmethod
    def set(email: str, timebucket: list[float], lockout_timestamp=None) -> None:
        key: str = InvalidLoginAttemptsCache._key(email)
        value: dict[str, list[float] | float] = InvalidLoginAttemptsCache._value(
            lockout_timestamp, timebucket
        )
        cache.set(key, value)

    @staticmethod
    def invalid_attempt(
        cache_results: dict, current_datetime: datetime.datetime, usr: str
    ) -> str | None:
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
            # TODO po co ten return skoro nic z tym nie robimy
            return "locked_user_login_attempts"
        InvalidLoginAttemptsCache.set(usr, invalid_attempt_timestamps)


def authenticate_login_credentials(email, password) -> (dict[str, Any], int):
    if not re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email):
        return EMAIL_WRONG_FORMAT_RESPONSE
    if not re.fullmatch(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%*?&_-]{10,50}$",
        password,
    ):
        return PASSWORD_WRONG_FORMAT_RESPONSE
    try:
        User.query.filter_by(email=email, password=password).first()
        if email in LOGGED_IN_USER_TOKENS.keys():
            return ALREADY_LOGGED_IN_RESPONSE, {"token": LOGGED_IN_USER_TOKENS[email]}
        token: str = create_access_token(identity=email)
        LOGGED_IN_USER_TOKENS[email] = token
        return LOGIN_SUCCESSFUL_RESPONSE, {"token": token}
    except User.DoesNotExist:
        logger.info("User does not exist")
    return USER_NOT_LOGGED_IN_RESPONSE


class Login(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("email")
        self.post_parser.add_arg("password")
        super(Login, self).__init__()

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        email: str = args.get("email")
        password: str = args.get("password")
        return create_response(authenticate_login(email, password))


def authenticate_login(email, password) -> dict[str, str | None]:
    current_datetime: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    cache_results: dict | None = InvalidLoginAttemptsCache.get(email)
    if cache_results and cache_results.get("lockout_start"):
        lockout_start_timestamp: float = cache_results.get("lockout_start")
        lockout_start: datetime.datetime = datetime.datetime.fromtimestamp(
            lockout_start_timestamp, datetime.timezone.utc
        )
        locked_out: bool = lockout_start >= (
            current_datetime + datetime.timedelta(minutes=-15)
        )
        if not locked_out:
            InvalidLoginAttemptsCache.delete(email)
        else:
            logger.warning(f"locked out user: {email}")
            return LOCKED_USER_LOGIN_ATTEMPTS_RESPONSE
    login_data: (dict[str, Any], int) = authenticate_login_credentials(
        email=email, password=password
    )
    # TODO czy tu nie powinno być if not logged_in? coś tu chyba nie gra
    if cache_results:
        InvalidLoginAttemptsCache.invalid_attempt(
            cache_results, current_datetime, email
        )
    return login_data
