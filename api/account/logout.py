from flask import Response
from flask_restful import Resource

from helpers.blocklist import LOGGED_IN_USER_TOKENS
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import create_response, RequestParser
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    LOGGED_OUT_RESPONSE,
    USER_NOT_FOUND_RESPONSE,
    USER_NOT_LOGGED_IN_RESPONSE,
)


class Logout(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("language", required=False)
        super(Logout, self).__init__()

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        language: str = args.get("language")
        try:
            email: str | None = verify_jwt_token()
            if not email:
                return create_response(TOKEN_INVALID_RESPONSE, language=language)
            LOGGED_IN_USER_TOKENS.pop(email)
            return create_response(LOGGED_OUT_RESPONSE, language=language)
        except KeyError:
            return create_response(USER_NOT_FOUND_RESPONSE, language=language)
        except AttributeError:
            return create_response(USER_NOT_LOGGED_IN_RESPONSE, language=language)
