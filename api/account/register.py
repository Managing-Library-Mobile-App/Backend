import re

from flask import Response
from flask_restful import Resource
from sqlalchemy import exists

from helpers.init import db
from helpers.request_response import RequestParser, create_response
from models.library import Library
from models.user import User
from static.responses import (
    EMAIL_WRONG_FORMAT_RESPONSE,
    PASSWORD_WRONG_FORMAT_RESPONSE,
    USER_ALREADY_EXISTS_RESPONSE,
    REGISTER_SUCCESSFUL_RESPONSE,
)


class Register(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("username")
        self.post_parser.add_arg("password")
        self.post_parser.add_arg("email")
        self.post_parser.add_arg("language", required=False)
        super(Register, self).__init__()

    def post(self) -> Response:
        args = self.post_parser.parse_args()
        username: str = args.get("username")
        password: str = args.get("password")
        email: str = args.get("email")
        language: str = args.get("language")
        if not re.fullmatch(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email
        ):
            return create_response(EMAIL_WRONG_FORMAT_RESPONSE, language=language)
        if not re.fullmatch(r"^[a-zA-Z0-9_-]{10,50}$", username):
            return create_response(EMAIL_WRONG_FORMAT_RESPONSE, language=language)
        if not re.fullmatch(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%*?&_-]{10,50}$",
            password,
        ):
            return create_response(PASSWORD_WRONG_FORMAT_RESPONSE, language=language)

        user_already_exists: bool = db.session.query(
            exists().where(User.email == email, User.username == username)
        ).scalar()

        if user_already_exists:
            return create_response(USER_ALREADY_EXISTS_RESPONSE, language=language)

        new_user: User = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        new_user_library: Library = Library(
            read_books=[], bought_books=[], favourite_books=[], user_id=new_user.id
        )
        db.session.add(new_user_library)
        db.session.commit()

        return create_response(REGISTER_SUCCESSFUL_RESPONSE, language=language)
