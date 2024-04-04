from flask import Response
from flask_restful import Resource

from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser
from models import user
from helpers.request_response import create_response
from static.responses import TOKEN_INVALID_RESPONSE, INSUFFICIENT_PERMISSIONS_RESPONSE, \
    USER_OBJECTS_LIST_RESPONSE, USER_OBJECT_RESPONSE, OBJECT_NOT_FOUND_RESPONSE


class User(Resource):
    def __init__(self) -> None:
        self.get_parser: RequestParser = RequestParser()
        self.get_parser.add_arg("id", type=int, required=False)
        super(User, self).__init__()

    def get(self) -> Response:
        args: dict = self.get_parser.parse_args()
        user_id: int = args.get("id")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE)
        current_user: user.User = user.User.query.filter_by(email=email).first()

        if user_id:
            user_object: user.User = user.User.query.filter_by(id=user_id).first()
            if not user_object:
                return create_response(OBJECT_NOT_FOUND_RESPONSE)
            if not current_user.is_admin and not current_user.id == user_object.id:
                return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE)
            return create_response(USER_OBJECT_RESPONSE,
                                   {"user": user_object.as_dict()}
                                   )
        else:
            user_objects: list[user.User] = user.User.query.all()
            return create_response(USER_OBJECTS_LIST_RESPONSE,
                                   {"users": [user_object.as_dict() for user_object in user_objects]},
                                   )
