from flask import Response, request
from flask_restful import Resource

from helpers.jwt_auth import verify_jwt_token
from models import user
from helpers.request_response import create_response
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    INSUFFICIENT_PERMISSIONS_RESPONSE,
    USERS_RESPONSE,
)


class User(Resource):
    def __init__(self) -> None:
        super(User, self).__init__()

    def get(self) -> Response:
        page: int = request.args.get("page", 1, type=int)
        per_page: int = request.args.get("per_page", 8, type=int)
        language: str = request.args.get("language", type=str)  # optional
        user_id: int = request.args.get("id", type=int)  # optional
        username: str = request.args.get("username", type=str)  # optional
        get_self: bool = request.args.get("get_self", type=bool)  # optional
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        filters_list = []
        if username:
            filters_list.append(user.User.username.ilike(f"%{username}%"))
        if get_self:
            filters_list.append(user.User.email == email)
        if user_id:
            filters_list.append(user.User.id == user_id)

        user_objects = user.User.query.filter(*filters_list).paginate(
            page=page, per_page=per_page
        )

        current_user: user.User = user.User.query.filter_by(email=email).first()
        if not current_user.is_admin and not (
            user_objects.total == 1 and current_user.id == user_objects[0].id
        ):
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        return create_response(
            USERS_RESPONSE,
            {
                "results": [user_object.as_dict() for user_object in user_objects],
                "pagination": {
                    "count": user_objects.total,
                    "page": page,
                    "pages": user_objects.pages,
                    "per_page": user_objects.per_page,
                },
            },
            language=language,
            not_translated={"username", "email", "password"},
        )
