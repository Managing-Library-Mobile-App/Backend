from flask import Response, make_response, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from helpers.blocklist import BLOCK_LIST_USERS
from helpers.jwt_auth import verify_jwt_token
from models.user import User


class LoggedInUsers(Resource):
    def __init__(self) -> None:
        super(LoggedInUsers, self).__init__()

    @jwt_required()
    def get(self) -> Response:
        verification_output = verify_jwt_token()
        if type(verification_output) is str:
            email = verification_output
        else:
            return make_response(verification_output, 401)

        user = User.query.filter_by(email=email).first()
        if user:
            if user.is_admin:
                return make_response(
                    jsonify(
                        logged_in_users=[user for user in BLOCK_LIST_USERS],
                    ),
                    200,
                )
            return make_response(
                jsonify(
                    password_changed=False,
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin account.",
                ),
                404,
            )
        return make_response(
            jsonify(
                password_changed=False,
                message="user_does_not_exist",
                details="User does not exist",
            ),
            404,
        )
