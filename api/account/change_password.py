from flask import Response, make_response, jsonify
from flask_jwt_extended import jwt_required
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
        """
        This examples uses FlaskRESTful Resource
        It works also with swag_from, schemas and spec_dict
        ---
        parameters:
        - in: body
          name: passwords
          description: The passwords.
          schema:
            type: object
            required:
              - current_password
              - new_password
            properties:
              current_password:
                type: string
              new_password:
                type: string
        consumes:
        - "application/json"
        produces:
        - "application/json"
        security:
        - APIKeyHeader: ['x-access-token']
        responses:
          200:
            description: A single user item
            schema:
              id: User
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
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
                message="wrong_password",
                details="Wrong password",
            ),
            401,
        )
