from flask import jsonify, Response, make_response
from flask_restful import Resource

from flask_jwt_extended import (
    jwt_required,
    verify_jwt_in_request,
    get_jwt_identity,
)

from helpers.blocklist import BLOCK_LIST_USERS


class Logout(Resource):
    def __init__(self) -> None:
        super(Logout, self).__init__()

    @jwt_required()
    def post(self) -> Response:
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            BLOCK_LIST_USERS.remove(current_user)
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
