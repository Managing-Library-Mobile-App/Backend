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
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE)
        auth: str | None = request.headers.get("Authorization")
        token: str = ""
        if auth:
            token = auth.split(" ")[1]
        if token in LOGGED_IN_USER_TOKENS.values():
            return create_response(TOKEN_VALID_RESPONSE)
        return create_response(TOKEN_INVALID_RESPONSE)
