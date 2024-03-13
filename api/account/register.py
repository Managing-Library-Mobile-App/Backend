import re

from flask import Response, jsonify, make_response
from loguru import logger
from flask_restful import Resource
from sqlalchemy import exists

from helpers.request_parser import RequestParser
from models.library import Library
from models.user import User
from helpers.init import db


def authenticate_register_credentials(
    username: str, password: str, email: str
) -> dict[str, str | None]:
    if not re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email):
        return {
            "message": "email_wrong_format",
            "details": "Wrong email format.",
        }
    if not re.fullmatch(r"^[a-zA-Z0-9_-]{10,50}$", username):
        return {
            "message": "username_wrong_format",
            "details": "Wrong username format. It should be from 10 to 50 characters "
            "and it can only contain upper letters, lower letters, "
            "numbers and signs: - and _",
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

    user_already_exists: bool = db.session.query(
        exists().where(User.email == email, User.username == username)
    ).scalar()

    if user_already_exists:
        return {
            "message": "user_already_exists",
            "details": "User already exists",
        }

    new_user: User = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    new_user_library: Library = Library(
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
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("username")
        self.post_parser.add_arg("password")
        self.post_parser.add_arg("email")
        super(Register, self).__init__()

    def post(self) -> Response:
        args = self.post_parser.parse_args()
        username: str = args.get("username")
        password: str = args.get("password")
        email: str = args.get("email")
        registration_output: dict[str, str | None] = authenticate_register_credentials(
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
