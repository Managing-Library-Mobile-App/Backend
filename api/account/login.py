from __future__ import annotations

import datetime
from typing import Any

from flask import jsonify, Response
from flask_jwt_extended import (
    get_jwt_identity,
    create_access_token,
    verify_jwt_in_request,
    jwt_required,
)
from flask_restful import reqparse  # type: ignore
from loguru import logger
from flask_restful import Resource

from helpers.init import cache
from api.account.register import (
    contains_uppercase_char,
    contains_illegal_char,
    contains_special_char,
)

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


def authenticate_login_credentials(username, password) -> dict[str, str | None | User]:
    if contains_illegal_char(username):
        return {
            "token": None,
            "message": "contains_illegal_char_username",
            "details": "Illegal characters in username such as space",
        }
    if not contains_special_char(password):
        return {
            "token": None,
            "message": "not_contains_special_char_password",
            "details": "No special characters in password. Required at least one",
        }
    if contains_illegal_char(password):
        return {
            "token": None,
            "message": "contains_illegal_char_password",
            "details": "Illegal characters in password such as space",
        }
    if not contains_uppercase_char(password):
        return {
            "token": None,
            "message": "not_contains_uppercase_char_password",
            "details": "Password has no uppercase letters. Required at least one.",
        }
    if len(username) < 10:
        return {
            "token": None,
            "message": "username_too_short",
            "details": "Password should have a minimum of 10 characters",
        }
    if len(username) > 50:
        return {
            "token": None,
            "message": "username_too_long",
            "details": "Password should have 50 characters max",
        }
    if len(password) < 10:
        return {
            "token": None,
            "message": "password_too_short",
            "details": "Password should have a minimum of 10 characters",
        }
    if len(password) > 50:
        return {
            "token": None,
            "message": "password_too_long",
            "details": "Password should have 50 characters max",
        }

    user = None
    try:
        user = User.query.filter_by(username=username, password=password).first()
    except User.DoesNotExist:
        logger.info("User does not exist")
    if user:
        access_token = create_access_token(identity=username)
        return {
            "token": access_token,
            "message": "login_successful",
            "details": "Login successful",
        }
    return {
        "token": None,
        "message": "authentication_failed",
        "details": "Wrong username or password",
    }


class Login(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            location="json",
        )
        self.reqparse.add_argument("password", type=str, required=True, location="json")
        super(Login, self).__init__()

    def post(self) -> tuple[Response, int]:
        args = self.reqparse.parse_args()
        username = args.get("username")
        password = args.get("password")
        login_output = authenticate_login(username, password)

        if isinstance(login_output["user"], User):
            logger.info(f"Zarejestrowano użytkownika {login_output['user']}")
            return (
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
            return (
                jsonify(
                    registered=False,
                    message=login_output["message"],
                    details=login_output["details"],
                ),
                401,
            )
        raise Exception("Unexpected login behavior! Raised exception!")


def authenticate_login(
    username, password
) -> dict[str, str | None] | dict[str, str | None | User]:
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
    InvalidLoginAttemptsCache.invalid_attempt(cache_results, current_datetime, username)
    return login_data


# TODO

# TODO jsonify przy zwracaniu wartości dla usera wraz z kodem odpowiedzi


class Protected(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        super(Protected, self).__init__()

    @jwt_required()
    def get(self) -> tuple[Response, int]:
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200


class CheckLogin(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        super(CheckLogin, self).__init__()

    def get(self) -> tuple[Response, int]:
        try:
            # Verify JWT token in the request
            verify_jwt_in_request()
            # If verification is successful, return the identity of the current user
            current_user = get_jwt_identity()
            return jsonify(logged_in_as=current_user), 200
        except Exception as e:
            # If verification fails or JWT token is missing, return a message indicating that the user is not logged in
            return jsonify(message="User not logged in"), 401
