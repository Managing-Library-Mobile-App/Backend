import re

from flask import Response
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser, APIArgument
from models.user import User
from helpers.request_response import create_response
from static.responses import (
    PASSWORD_WRONG_FORMAT_RESPONSE,
    PASSWORD_CHANGED_RESPONSE,
    PASSWORD_NOT_CHANGED_RESPONSE,
    TOKEN_INVALID_RESPONSE,
)


class ChangePassword(Resource):
    def __init__(self) -> None:
        self.patch_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.patch_parser.add_arg("current_password")
        self.patch_parser.add_arg("new_password")
        self.patch_parser.add_arg("language", required=False)
        super(ChangePassword, self).__init__()

    def patch(self) -> Response:
        args: dict = self.patch_parser.parse_args()
        current_password: str = args.get("current_password")
        new_password: str = args.get("new_password")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        if not re.fullmatch(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%*?&_-]{10,50}$",
            new_password,
        ):
            return create_response(PASSWORD_WRONG_FORMAT_RESPONSE, language=language)

        user: User = User.query.filter_by(
            email=email, password=current_password
        ).first()
        if user:
            user.password = new_password
            db.session.commit()
            return create_response(
                PASSWORD_CHANGED_RESPONSE, user.as_dict(), language=language
            )
        return create_response(PASSWORD_NOT_CHANGED_RESPONSE, language=language)
