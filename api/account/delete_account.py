from flask import Response, make_response, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_restful import Resource
from api.account.blocklist import BLOCK_LIST_USERS
from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_parser import RequestParser
from models.user import User


class DeleteAccount(Resource):
    def __init__(self) -> None:
        self.delete_parser = RequestParser()
        self.delete_parser.add_arg("password")
        super(DeleteAccount, self).__init__()

    def delete(self) -> Response:
        args = self.delete_parser.parse_args()
        password = args.get("password")
        verification_output = verify_jwt_token()
        if type(verification_output) is str:
            email = verification_output
        else:
            return make_response(verification_output, 401)

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
