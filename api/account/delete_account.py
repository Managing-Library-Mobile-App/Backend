from flask import Response
from flask_restful import Resource

from helpers.blocklist import LOGGED_IN_USER_TOKENS
from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_parser import RequestParser
from models.user import User
from static.responses import create_response, TOKEN_INVALID_RESPONSE, CANNOT_DELETE_ADMIN_RESPONSE, \
    USER_DELETED_RESPONSE, USER_DOES_NOT_EXIST_RESPONSE


class DeleteAccount(Resource):
    def __init__(self) -> None:
        self.delete_parser: RequestParser = RequestParser()
        self.delete_parser.add_arg("password")
        super(DeleteAccount, self).__init__()

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        password: str = args.get("password")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE)

        user: User = User.query.filter_by(email=email, password=password).first()

        if user.is_admin:
            return create_response(CANNOT_DELETE_ADMIN_RESPONSE)

        if user:
            LOGGED_IN_USER_TOKENS.pop(email)
            db.session.delete(user)
            db.session.commit()
            return create_response(USER_DELETED_RESPONSE)
        return create_response(USER_DOES_NOT_EXIST_RESPONSE)
