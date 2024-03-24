from flask import Response
from flask_restful import Resource

from helpers.blocklist import LOGGED_IN_USER_TOKENS
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import create_response
from static.responses import TOKEN_INVALID_RESPONSE, LOGGED_OUT_RESPONSE, USER_NOT_FOUND_RESPONSE, \
    USER_NOT_LOGGED_IN_RESPONSE


class Logout(Resource):
    def __init__(self) -> None:
        super(Logout, self).__init__()

    def post(self) -> Response:
        try:
            email: str | None = verify_jwt_token()
            if not email:
                return create_response(TOKEN_INVALID_RESPONSE)
            LOGGED_IN_USER_TOKENS.pop(email)
            return create_response(LOGGED_OUT_RESPONSE)
        except KeyError:
            return create_response(USER_NOT_FOUND_RESPONSE)
        except AttributeError:
            return create_response(USER_NOT_LOGGED_IN_RESPONSE)
