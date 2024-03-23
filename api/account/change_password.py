import re

from flask import Response
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_parser import RequestParser
from models.user import User
from static.responses import create_response, PASSWORD_WRONG_FORMAT_RESPONSE, PASSWORD_CHANGED_RESPONSE, \
    PASSWORD_NOT_CHANGED_RESPONSE, TOKEN_INVALID_RESPONSE


class ChangePassword(Resource):
    def __init__(self) -> None:
        self.patch_parser: RequestParser = RequestParser()
        self.patch_parser.add_arg("current_password")
        self.patch_parser.add_arg("new_password")
        super(ChangePassword, self).__init__()

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
              properties:
                password_changed:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: password_changed
                details:
                  type: string
                  example: Password changed
          401:
            schema:
              properties:
                password_changed:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: wrong_password
                details:
                  type: string
                  example: Wrong password
          403:
            schema:
              properties:
                password_changed:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: password_wrong_format
                details:
                  type: string
                  example: Wrong password format. Password should have from 10 to 50 characters.
                        It should contain at least one upper letter, at least 1 lower letter, at least 1 number and
                        at least one special character

        """
        args: dict = self.patch_parser.parse_args()
        current_password: str = args.get("current_password")
        new_password: str = args.get("new_password")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE)

        if not re.fullmatch(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%*?&_-]{10,50}$",
            new_password,
        ):
            return create_response(PASSWORD_WRONG_FORMAT_RESPONSE)

        user: User = User.query.filter_by(
            email=email, password=current_password
        ).first()
        if user:
            user.password = new_password
            db.session.commit()

            return create_response(PASSWORD_CHANGED_RESPONSE)
        return create_response(PASSWORD_NOT_CHANGED_RESPONSE)
