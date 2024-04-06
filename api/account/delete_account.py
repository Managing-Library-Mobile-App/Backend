from flask import Response
from flask_restful import Resource

from helpers.blocklist import LOGGED_IN_USER_TOKENS
from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser
from models.user import User
from helpers.request_response import create_response
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    CANNOT_DELETE_ADMIN_RESPONSE,
    USER_DELETED_RESPONSE,
    USER_DOES_NOT_EXIST_RESPONSE,
    INVALID_PASSWORD_RESPONSE,
)


class DeleteAccount(Resource):
    def __init__(self) -> None:
        self.delete_parser: RequestParser = RequestParser()
        self.delete_parser.add_arg("password")
        self.delete_parser.add_arg("language", required=False)
        super(DeleteAccount, self).__init__()

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        password: str = args.get("password")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if password != user.password:
            return create_response(INVALID_PASSWORD_RESPONSE, language=language)
        if user:
            if user.is_admin:
                db.session.delete(user)
                return create_response(CANNOT_DELETE_ADMIN_RESPONSE, language=language)
            LOGGED_IN_USER_TOKENS.pop(email)
            db.session.delete(user)
            db.session.commit()
            return create_response(USER_DELETED_RESPONSE, language=language)
        return create_response(USER_DOES_NOT_EXIST_RESPONSE, language=language)
