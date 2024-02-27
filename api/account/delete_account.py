from flask import Response, make_response, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_restful import Resource, reqparse

from api.account.blocklist import BLOCK_LIST_USERS
from helpers.init import db
from models.user import User


class DeleteAccount(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "password",
            type=str,
            required=True,
            location="json",
        )
        super(DeleteAccount, self).__init__()

    def delete(self) -> Response:
        args = self.reqparse.parse_args()
        password = args.get("password")
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

        user = User.query.filter_by(email=email, password=password).first()

        if user.is_admin:
            return make_response(
                jsonify(
                    password_changed=False,
                    message="cannot_delete_admin",
                    details="Admin account cannot be deleted",
                ),
                404,
            )

        if user:
            print(BLOCK_LIST_USERS)
            BLOCK_LIST_USERS.remove(email)
            db.session.delete(user)
            db.session.commit()
            return make_response(
                jsonify(
                    password_changed=True,
                    message="user_deleted",
                    details="User deleted successfully",
                ),
                200,
            )
        return make_response(
            jsonify(
                password_changed=False,
                message="user_does_not_exist",
                details="User does not exist",
            ),
            404,
        )
