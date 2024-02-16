from __future__ import annotations

import re
import string

from flask import Response, jsonify
from flask_restful import reqparse  # type: ignore
from loguru import logger
from flask_restful import Resource
from sqlalchemy import exists

from models.library import Library
from models.user import User
from helpers.init import db


def contains_special_char(characters: str) -> bool:
    for character in characters:
        if character in string.punctuation:
            return True
    return False


def contains_illegal_char(characters: str) -> bool:
    if characters.__contains__(" "):
        return True
    return False


def contains_uppercase_char(characters: str) -> bool:
    if characters.lower() == characters:
        return False
    return True


def authenticate_register_credentials(
    username: str, password: str, email: str
) -> dict[str, str | None | User]:
    if contains_illegal_char(username):
        return {
            "message": "contains_illegal_char_username",
            "details": "Illegal characters in username such as space",
        }
    if not contains_special_char(password):
        return {
            "message": "not_contains_special_char_password",
            "details": "No special characters in password. Required at least one",
        }
    if contains_illegal_char(password):
        return {
            "message": "contains_illegal_char_password",
            "details": "Illegal characters in password such as space",
        }
    if not contains_uppercase_char(password):
        return {
            "message": "not_contains_uppercase_char_password",
            "details": "Password has no uppercase letters. Required at least one.",
        }
    if len(username) < 10:
        return {
            "message": "username_too_short",
            "details": "Username should have a minimum of 10 characters",
        }
    if len(username) > 50:
        return {
            "message": "username_too_long",
            "details": "Username should have 50 characters max",
        }
    if len(password) < 10:
        return {
            "message": "password_too_short",
            "details": "Password should have a minimum of 10 characters",
        }
    if len(password) > 50:
        return {
            "message": "password_too_long",
            "details": "Passwrod should have 50 characters max",
        }
    if len(email) > 50:
        return {
            "message": "email_too_long",
            "details": "Email should have 50 characters max",
        }
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(regex, email):
        return {
            "message": "email_of_wrong_format",
            "details": "User already exists",
        }

    user_already_exists = db.session.query(
        exists().where(User.username == username, User.email == email)
    ).scalar()

    if user_already_exists:
        return {
            "message": "user_already_exists",
            "details": "User already exists",
        }

    new_user_library = Library()
    db.session.add(new_user_library)
    db.session.commit()

    new_user = User(
        username=username,
        password=password,
        email=email,
        library_id=new_user_library.id,
    )
    db.session.add(new_user)
    db.session.commit()

    return {
        "message": "register_successful",
        "details": "Register successful",
    }


class Register(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            location="json",
        )
        self.reqparse.add_argument("password", type=str, required=True, location="json")
        self.reqparse.add_argument("email", type=str, required=True, location="json")
        super(Register, self).__init__()

    def post(self) -> tuple[Response, int]:
        args = self.reqparse.parse_args()
        username = args.get("username")
        password = args.get("password")
        email = args.get("email")
        registration_output = authenticate_register_credentials(
            username=username, password=password, email=email
        )
        if registration_output["message"] == "register_successful":
            logger.info(f"Zarejestrowano użytkownika {username}")
            return (
                jsonify(
                    message=str(registration_output["message"]),
                    details=str(registration_output["details"]),
                ),
                200,
            )
        logger.info(
            f"Nieudana próba rejestracji użytkownika. {registration_output['message']}"
        )
        return (
            jsonify(
                message=str(registration_output["message"]),
                details=str(registration_output["details"]),
            ),
            401,
        )
