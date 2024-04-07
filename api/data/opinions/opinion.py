from flask import Response, request
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser
from models import opinion
from models.user import User
from helpers.request_response import create_response
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    INSUFFICIENT_PERMISSIONS_RESPONSE,
    OBJECT_CREATED_RESPONSE,
    OBJECT_DELETED_RESPONSE,
    OBJECT_MODIFIED_RESPONSE,
    OPINION_OBJECT_RESPONSE,
    OPINION_OBJECTS_LIST_RESPONSE,
    OBJECT_NOT_FOUND_RESPONSE,
)


class Opinion(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("user_id", type=int)
        self.post_parser.add_arg("book_id", type=int)
        self.post_parser.add_arg("stars_count", type=int)
        self.post_parser.add_arg("comment")
        self.post_parser.add_arg("language", required=False)
        self.delete_parser: RequestParser = RequestParser()
        self.delete_parser.add_arg("id", type=int)
        self.delete_parser.add_arg("language", required=False)
        self.patch_parser: RequestParser = RequestParser()
        self.patch_parser.add_arg("id", type=int)
        self.patch_parser.add_arg("stars_count", type=int, required=False)
        self.patch_parser.add_arg("comment", type=str, required=False)
        self.patch_parser.add_arg("language", required=False)
        super(Opinion, self).__init__()

    def get(self) -> Response:
        language: str = request.args.get("language")
        opinion_id: str = request.args.get("id")
        if opinion_id:
            try:
                opinion_id: int = int(opinion_id)
            except ValueError:
                return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if opinion_id:
            opinion_object: opinion.Opinion = opinion.Opinion.query.filter_by(
                id=opinion_id
            ).first()
            if not opinion_object:
                return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
            if not user.id == opinion_object.user_id and not user.is_admin:
                return create_response(
                    INSUFFICIENT_PERMISSIONS_RESPONSE, language=language
                )
            return create_response(
                OPINION_OBJECT_RESPONSE, opinion_object.as_dict(), language=language
            )
        opinion_objects: list[opinion.Opinion] = opinion.Opinion.query.all()
        return create_response(
            OPINION_OBJECTS_LIST_RESPONSE,
            {
                "opinions": [
                    opinion_object.as_dict() for opinion_object in opinion_objects
                ]
            },
            language=language,
        )

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        user_id: int = args.get("user_id")
        book_id: int = args.get("book_id")
        stars_count: int = args.get("stars_count")
        comment: str = args.get("comment")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        # TODO A CO JEŚLI USER O TAKIM ID LUB KSIĄŻKA NIE ISTNIEJE?
        opinion_object: opinion.Opinion = opinion.Opinion(
            user_id=user_id,
            book_id=book_id,
            stars_count=stars_count,
            comment=comment,
        )
        db.session.add(opinion_object)
        db.session.commit()

        return create_response(OBJECT_CREATED_RESPONSE, language=language)

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        opinion_id: int = args.get("id")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()

        opinion_object: opinion.Opinion = opinion.Opinion.query.filter_by(
            id=opinion_id
        ).first()
        if not opinion_object:
            return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
        if not user.is_admin and user.id != opinion_object.user_id:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        db.session.delete(opinion_object)
        db.session.commit()

        return create_response(OBJECT_DELETED_RESPONSE, language=language)

    def patch(self) -> Response:
        args: dict = self.patch_parser.parse_args()
        opinion_id: int = args.get("id")
        stars_count: int = args.get("stars_count")
        comment: str = args.get("comment")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        modified_opinion = opinion.Opinion.query.filter_by(id=opinion_id).first()

        if user:
            if stars_count:
                modified_opinion.stars_count = stars_count
            if comment:
                modified_opinion.comment = comment
            db.session.commit()

        return create_response(OBJECT_MODIFIED_RESPONSE, language=language)
