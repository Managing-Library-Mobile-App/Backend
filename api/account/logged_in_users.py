import os

from flask import Response, request
from flask_restful import Resource

from helpers.blocklist import LOGGED_IN_USER_TOKENS
from helpers.request_response import create_response
from static.responses import WRONG_SECRET_RESPONSE, LOGGED_IN_USERS_RESPONSE


class LoggedInUsers(Resource):
    def __init__(self) -> None:
        super(LoggedInUsers, self).__init__()

    def get(self) -> Response:
        secret: str = request.args.get("secret")
        language: str = request.args.get("language")
        if secret == os.environ.get("secret"):
            return create_response(
                LOGGED_IN_USERS_RESPONSE,
                {
                    "logged_in_users": {
                        email: LOGGED_IN_USER_TOKENS[email]
                        for email in LOGGED_IN_USER_TOKENS.keys()
                    }
                },
                language=language,
                not_translated={"logged_in_users"},
            )
        return create_response(WRONG_SECRET_RESPONSE, language=language)
