from flask import Response
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser, APIArgument, int_range_validation
from models.user import User
from helpers.request_response import create_response
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    MOTIVE_CHANGED_RESPONSE,
    MOTIVE_NOT_CHANGED_RESPONSE,
)


class ChangeTheme(Resource):
    def __init__(self) -> None:
        self.patch_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.patch_parser.add_arg("theme", type=int_range_validation(min=1, max=3))
        self.patch_parser.add_arg("language", required=False)
        super(ChangeTheme, self).__init__()

    def patch(self) -> Response:
        args: dict = self.patch_parser.parse_args()
        theme: int = args.get("theme")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        user: User = User.query.filter_by(email=email).first()
        if user:
            user.theme = theme
            db.session.commit()
            return create_response(MOTIVE_CHANGED_RESPONSE, language=language)
        return create_response(MOTIVE_NOT_CHANGED_RESPONSE, language=language)