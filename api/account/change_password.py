from flask import Response, make_response, jsonify
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_restful import Resource, reqparse

from helpers.init import db
from models.user import User


class ChangePassword(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "current_password",
            type=str,
            required=True,
            location="json",
        )
        self.reqparse.add_argument(
            "new_password",
            type=str,
            required=True,
            location="json",
        )
        super(ChangePassword, self).__init__()

    @jwt_required()
    def patch(self) -> Response:
        args = self.reqparse.parse_args()
        current_password = args.get("current_password")
        new_password = args.get("new_password")
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

        user = User.query.filter_by(email=email, password=current_password).first()
        if user:
            user.password = new_password
            db.session.commit()

            return make_response(
                jsonify(
                    password_changed=True,
                    message="password_changed",
                    details="Password changed successfully",
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
