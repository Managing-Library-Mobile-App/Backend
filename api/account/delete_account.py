from flask import Response, make_response, jsonify
from flask_restful import Resource
from helpers.blocklist import LOGGED_IN_USER_TOKENS
from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_parser import RequestParser
from models.user import User


class DeleteAccount(Resource):
    def __init__(self) -> None:
        self.delete_parser: RequestParser = RequestParser()
        self.delete_parser.add_arg("password")
        super(DeleteAccount, self).__init__()

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        password: str = args.get("password")
        verification_output: Response | str = verify_jwt_token()
        if type(verification_output) is str:
            email: str = verification_output
        else:
            return make_response(verification_output, 401)

        user: User = User.query.filter_by(email=email, password=password).first()

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
            print(LOGGED_IN_USER_TOKENS)
            LOGGED_IN_USER_TOKENS.pop(email)
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
