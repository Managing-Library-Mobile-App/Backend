from flask import Response, make_response, jsonify
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_restful import Resource

from api.account.blocklist import BLOCK_LIST_USERS
from models.user import User


class LoggedInUsers(Resource):
    def __init__(self) -> None:
        super(LoggedInUsers, self).__init__()

    @jwt_required()
    def get(self) -> Response:
        try:
            verify_jwt_in_request()
            email = get_jwt_identity()
        except AttributeError:
            return make_response(
                jsonify(
                    password_changed=False,
                    message="user_not_logged_in",
                    details="User not logged in (No session)",
                ),
                401,
            )

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
