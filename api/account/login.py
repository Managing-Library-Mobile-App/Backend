import datetime
import re
from typing import Any

from flask import Response
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from loguru import logger

from helpers.blocklist import LOGGED_IN_USER_TOKENS
from helpers.init import cache
from helpers.request_response import RequestParser, create_response, APIArgument
from models.user import User
from static.responses import (
    USER_NOT_LOGGED_IN_RESPONSE,
    LOCKED_USER_LOGIN_ATTEMPTS_RESPONSE,
    PASSWORD_WRONG_FORMAT_RESPONSE,
    EMAIL_WRONG_FORMAT_RESPONSE,
    ALREADY_LOGGED_IN_RESPONSE,
    LOGIN_SUCCESSFUL_RESPONSE,
)


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
        cache_results: dict, current_datetime: datetime.datetime, email: str
    ) -> None:
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
                email, invalid_attempt_timestamps, current_datetime.timestamp()
            )
        InvalidLoginAttemptsCache.set(email, invalid_attempt_timestamps)


def authenticate_login_credentials(
    email: str,
    password: str,
    language: str,
    cache_results: dict | None,
    current_datetime: datetime.datetime,
) -> (dict[str, Any], int):
    if not re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email):
        InvalidLoginAttemptsCache.invalid_attempt(
            cache_results, current_datetime, email
        )
        return create_response(EMAIL_WRONG_FORMAT_RESPONSE, language=language)
    if not re.fullmatch(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%*?&_-]{10,50}$",
        password,
    ):
        InvalidLoginAttemptsCache.invalid_attempt(
            cache_results, current_datetime, email
        )
        return create_response(PASSWORD_WRONG_FORMAT_RESPONSE, language=language)
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        if email in LOGGED_IN_USER_TOKENS.keys():
            return create_response(
                ALREADY_LOGGED_IN_RESPONSE,
                {"token": LOGGED_IN_USER_TOKENS[email]},
                language=language,
                not_translated={"token"},
            )
        token: str = create_access_token(
            identity=email, expires_delta=datetime.timedelta(days=30)
        )
        LOGGED_IN_USER_TOKENS[email] = token
        return create_response(
            LOGIN_SUCCESSFUL_RESPONSE,
            {"token": token},
            language=language,
            not_translated={"token"},
        )
    InvalidLoginAttemptsCache.invalid_attempt(cache_results, current_datetime, email)
    return create_response(USER_NOT_LOGGED_IN_RESPONSE, language=language)


class Login(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.post_parser.add_arg("email")
        self.post_parser.add_arg("password")
        self.post_parser.add_arg("language", required=False)
        super(Login, self).__init__()

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        email: str = args.get("email")
        password: str = args.get("password")
        language: str = args.get("language")
        current_datetime: datetime.datetime = datetime.datetime.now(
            datetime.timezone.utc
        )
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
                return create_response(
                    LOCKED_USER_LOGIN_ATTEMPTS_RESPONSE, language=language
                )
        login_data: (dict[str, Any], int) = authenticate_login_credentials(
            email=email,
            password=password,
            language=language,
            cache_results=cache_results,
            current_datetime=current_datetime,
        )
        return login_data
