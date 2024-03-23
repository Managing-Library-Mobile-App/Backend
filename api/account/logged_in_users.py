import os

from flask import Response, jsonify, make_response
from flask_restful import Resource

from helpers.blocklist import LOGGED_IN_USER_TOKENS
from helpers.request_parser import RequestParser
from static.responses import create_response, WRONG_SECRET_RESPONSE, LOGGED_IN_USERS_RESPONSE


class LoggedInUsers(Resource):
    def __init__(self) -> None:
        self.get_parser: RequestParser = RequestParser()
        self.get_parser.add_arg("secret")
        super(LoggedInUsers, self).__init__()

    def get(self) -> Response:
        args: dict = self.get_parser.parse_args()
        secret: str = args.get("secret")
        if secret == os.environ.get("secret"):
            return create_response(
                LOGGED_IN_USERS_RESPONSE,
                {"logged_in_users": {
                    email: LOGGED_IN_USER_TOKENS[email]
                    for email in LOGGED_IN_USER_TOKENS.keys()
                }},
            )
        return create_response(WRONG_SECRET_RESPONSE)
