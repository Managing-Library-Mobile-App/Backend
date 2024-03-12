from flask import jsonify, Response, make_response
from flask_restful import Resource

from helpers.blocklist import LOGGED_IN_USER_TOKENS
from helpers.jwt_auth import verify_jwt_token


class Logout(Resource):
    def __init__(self) -> None:
        super(Logout, self).__init__()

    def post(self) -> Response:
        try:
            verification_output = verify_jwt_token()

            if type(verification_output) is str:
                current_user = verification_output
            else:
                raise ValueError()
            LOGGED_IN_USER_TOKENS.pop(current_user)
            return make_response(jsonify(message="logged_out"), 200)
        except KeyError:
            return make_response(
                jsonify(
                    already_logged_in_as=None,
                    message="User logged in with such token not found.",
                ),
                401,
            )
        except AttributeError:
            return make_response(
                jsonify(already_logged_in_as=None, message="Could not log out user."),
                401,
            )
