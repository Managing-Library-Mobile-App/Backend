from flask import Response, request
from flask_restful import Resource

from helpers.blocklist import LOGGED_IN_USER_TOKENS
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import create_response
from static.responses import TOKEN_INVALID_RESPONSE, TOKEN_VALID_RESPONSE


class CheckIfLoggedIn(Resource):
    def __init__(self) -> None:
        super(CheckIfLoggedIn, self).__init__()

    def get(self) -> Response:
        language: str = request.args.get("language")
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        auth: str | None = request.headers.get("Authorization")
        if auth:
            token: str = auth.split(" ")[1]
            if token in LOGGED_IN_USER_TOKENS.values():
                return create_response(TOKEN_VALID_RESPONSE, language=language)
        return create_response(TOKEN_INVALID_RESPONSE, language=language)
