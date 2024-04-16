from flask import Response, request
from flask_restful import Resource

from helpers.jwt_auth import verify_jwt_token
from models import user
from helpers.request_response import create_response
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    INSUFFICIENT_PERMISSIONS_RESPONSE,
    OBJECT_NOT_FOUND_RESPONSE,
    USERS_RESPONSE,
    PARAM_NOT_INT_RESPONSE,
)


class User(Resource):
    def __init__(self) -> None:
        super(User, self).__init__()

    def get(self) -> Response:
        language: str = request.args.get("language")  # optional
        user_id: str = request.args.get("id")  # optional
        username: str = request.args.get("username")  # optional
        get_self: bool = bool(request.args.get("get_self"))  # optional
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        if user_id:
            try:
                user_id: int = int(user_id)
            except ValueError:
                return create_response(PARAM_NOT_INT_RESPONSE, language=language)

        filters_list = []
        if username:
            filters_list.append(user.User.username.ilike(f"%{username}%"))
        if get_self:
            filters_list.append(user.User.email == email)
        if user_id:
            filters_list.append(user.User.id == user_id)

        user_objects: list[user.User] = user.User.query.filter(*filters_list).all()

        current_user: user.User = user.User.query.filter_by(email=email).first()
        if not current_user.is_admin and not (
            len(user_objects) == 1 and current_user.id == user_objects[0].id
        ):
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        return create_response(
            USERS_RESPONSE,
            [user_object.as_dict() for user_object in user_objects]
            if len(user_objects) > 1
            else user_objects[0].as_dict()
            if len(user_objects) == 1
            else [],
            language=language,
            not_translated={"username", "email", "password"},
        )
