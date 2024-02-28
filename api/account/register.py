from __future__ import annotations

import re
import string

from flask import Response, jsonify, make_response
from loguru import logger
from flask_restful import Resource
from sqlalchemy import exists

from helpers.request_parser import RequestParser
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
) -> dict[str, str | None]:
    if contains_illegal_char(email):
        return {
            "message": "contains_illegal_char_email",
            "details": "Illegal characters in email such as space",
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
    if len(email) < 10:
        return {
            "message": "email_too_short",
            "details": "email should have a minimum of 10 characters",
        }
    if len(email) > 50:
        return {
            "message": "email_too_long",
            "details": "email should have 50 characters max",
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
            "message": "email_wrong_format",
            "details": "Wrong email format",
        }

    user_already_exists = db.session.query(
        exists().where(User.email == email, User.username == username)
    ).scalar()

    if user_already_exists:
        return {
            "message": "user_already_exists",
            "details": "User already exists",
        }

    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    new_user_library = Library(
        read_books=[], bought_books=[], favourite_books=[], user_id=new_user.id
    )
    db.session.add(new_user_library)
    db.session.commit()

    return {
        "message": "register_successful",
        "details": "Register successful",
    }


class Register(Resource):
    def __init__(self) -> None:
        self.post_parser = RequestParser()
        self.post_parser.add_arg("username")
        self.post_parser.add_arg("password")
        self.post_parser.add_arg("email")
        super(Register, self).__init__()

    def post(self) -> Response:
        args = self.post_parser.parse_args()
        username = args.get("username")
        password = args.get("password")
        email = args.get("email")
        logger.info(username, password, email)
        registration_output = authenticate_register_credentials(
            username=username, password=password, email=email
        )
        if registration_output["message"] == "register_successful":
            logger.info(f"Zarejestrowano użytkownika {username}")
            return make_response(
                jsonify(
                    message=str(registration_output["message"]),
                    details=str(registration_output["details"]),
                ),
                200,
            )
        logger.info(
            f"Nieudana próba rejestracji użytkownika. {registration_output['message']}"
        )
        return make_response(
            jsonify(
                message=str(registration_output["message"]),
                details=str(registration_output["details"]),
            ),
            401,
        )
