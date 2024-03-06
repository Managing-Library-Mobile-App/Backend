from flask import Response, make_response, jsonify
from flask_restful import Resource

from helpers.blocklist import BLOCKED_USER_TOKENS
from helpers.request_parser import RequestParser


class LoggedInUsers(Resource):
    def __init__(self) -> None:
        self.get_parser = RequestParser()
        self.get_parser.add_arg("secret")
        super(LoggedInUsers, self).__init__()

    def get(self) -> Response:
        args = self.get_parser.parse_args()
        secret = args.get("secret")
        if secret == "admin":
            return make_response(
                jsonify(
                    logged_in_users=[user for user in BLOCKED_USER_TOKENS],
                ),
                200,
            )
        return make_response(
            jsonify(
                message="wrong_secret",
                details="Wrong secret. Cannot view logged in users.",
            ),
            401,
        )
