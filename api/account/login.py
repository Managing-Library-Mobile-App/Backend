import datetime
import re
from typing import Any

from flask import jsonify, Response, make_response
from flask_jwt_extended import create_access_token
from loguru import logger
from flask_restful import Resource

from helpers.blocklist import LOGGED_IN_USER_TOKENS
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
            return "locked_user_login_attempts"
        InvalidLoginAttemptsCache.set(usr, invalid_attempt_timestamps)


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

    user: User | None = None
    try:
        user = User.query.filter_by(email=email, password=password).first()
    except User.DoesNotExist:
        logger.info("User does not exist")
    if user:
        if email in LOGGED_IN_USER_TOKENS.keys():
            return {
                "token": LOGGED_IN_USER_TOKENS[email],
                "message": "already_logged_in",
                "details": "Login already_logged_in",
            }
        token: str = create_access_token(identity=email)
        LOGGED_IN_USER_TOKENS[email] = token
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
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("email")
        self.post_parser.add_arg("password")
        super(Login, self).__init__()

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        email: str = args.get("email")
        password: str = args.get("password")
        login_output: dict[str, str | None] = authenticate_login(email, password)
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
        elif login_output["message"] == "already_logged_in":
            return make_response(
                jsonify(
                    token=login_output["token"],
                    message="user_already_logged_in",
                    details="User already logged in",
                ),
                401,
            )
        logger.info(
            f"Nieudana próba logowania użytkownika. {login_output['message']}, {login_output['details']}"
        )
        return make_response(
            jsonify(
                token=None,
                message=login_output["message"],
                details=login_output["details"],
            ),
            401,
        )


def authenticate_login(email, password) -> dict[str, str | None]:
    current_datetime: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    cache_results: dict | None = InvalidLoginAttemptsCache.get(email)
    logger.info(cache_results)
    logger.info(type(cache_results))
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
            return {
                "user": None,
                "message": "locked_user_login_attempts",
                "details": "User locked because of too many unsuccessful attempts",
            }
    login_data: dict[str, str | None] = authenticate_login_credentials(
        email=email, password=password
    )
    if cache_results:
        InvalidLoginAttemptsCache.invalid_attempt(
            cache_results, current_datetime, email
        )
    return login_data
