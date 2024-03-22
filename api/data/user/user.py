from flask import Response, jsonify, make_response
from flask_restful import Resource

from helpers.jwt_auth import verify_jwt_token
from helpers.request_parser import RequestParser
from models import user


class User(Resource):
    def __init__(self) -> None:
        self.get_parser: RequestParser = RequestParser()
        self.get_parser.add_arg("id", type=int, required=False)
        super(User, self).__init__()

    def get(self) -> Response:
        args: dict = self.get_parser.parse_args()
        user_id: int = args.get("id")
        verification_output: Response | str = verify_jwt_token()
        if type(verification_output) is str:
            email: str = verification_output
        else:
            return make_response(verification_output, 401)
        current_user: user.User = user.User.query.filter_by(email=email).first()
        if not current_user.is_admin:
            return make_response(
                jsonify(
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin or being the user",
                ),
                404,
            )

        if user_id:
            user_object: user.User = user.User.query.filter_by(id=user_id).first()
            return make_response(
                jsonify(user_object.as_dict()),
                200,
            )
        else:
            user_objects: list[user.User] = user.User.query.all()
            return make_response(
                jsonify(*[user_object.as_dict() for user_object in user_objects]),
                200,
            )
