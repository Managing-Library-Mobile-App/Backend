from flask import Response, request
from flask_restful import Resource

from helpers.jwt_auth import verify_jwt_token
from models import user
from helpers.request_response import create_response
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    INSUFFICIENT_PERMISSIONS_RESPONSE,
    USER_OBJECTS_LIST_RESPONSE,
    USER_OBJECT_RESPONSE,
    WRONG_LOGIN_PARAMS_COMBINATION,
    OBJECT_NOT_FOUND_RESPONSE,
)


class User(Resource):
    def __init__(self) -> None:
        super(User, self).__init__()

    def get(self) -> Response:
        not_translated: set[str] = {"username", "email", "password"}
        user_id = request.args.get("id")
        language: str = request.args.get("language")
        get_self: bool = bool(request.args.get("get_self"))
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        current_user: user.User = user.User.query.filter_by(email=email).first()
        if get_self and user_id:
            return create_response(WRONG_LOGIN_PARAMS_COMBINATION)
        if get_self:
            user_object: user.User = user.User.query.filter_by(email=email).first()
            return create_response(
                USER_OBJECT_RESPONSE, {"user": user_object.as_dict()}
            )
        if not current_user.is_admin:
            return INSUFFICIENT_PERMISSIONS_RESPONSE

        if user_id:
            user_object: user.User = user.User.query.filter_by(id=user_id).first()
            if not user_object:
                return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
            if not current_user.is_admin and not current_user.id == user_object.id:
                return create_response(
                    INSUFFICIENT_PERMISSIONS_RESPONSE, language=language
                )
            return create_response(
                USER_OBJECT_RESPONSE,
                {"user": user_object.as_dict()},
                language=language,
                not_translated=not_translated,
            )
        else:
            user_objects: list[user.User] = user.User.query.all()
            return create_response(
                USER_OBJECTS_LIST_RESPONSE,
                {"users": [user_object.as_dict() for user_object in user_objects]},
                language=language,
                not_translated=not_translated,
            )
