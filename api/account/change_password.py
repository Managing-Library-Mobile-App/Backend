from flask import Response, make_response, jsonify
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_parser import RequestParser
from models.user import User


class ChangePassword(Resource):
    def __init__(self) -> None:
        self.patch_parser = RequestParser()
        self.patch_parser.add_arg("current_password")
        self.patch_parser.add_arg("new_password")
        super(ChangePassword, self).__init__()

    @jwt_required()
    def patch(self) -> Response:
        args = self.patch_parser.parse_args()
        current_password = args.get("current_password")
        new_password = args.get("new_password")
        verification_output = verify_jwt_token()
        if type(verification_output) is str:
            email = verification_output
        else:
            return make_response(verification_output, 401)

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
