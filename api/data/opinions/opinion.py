import datetime

from flask import Response, request
from flask_restful import Resource
from sqlalchemy import desc

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import (
    RequestParser,
    int_range_validation,
    string_range_validation,
    APIArgument,
)
from models import opinion, book, user
from models.user import User
from helpers.request_response import create_response
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    INSUFFICIENT_PERMISSIONS_RESPONSE,
    OBJECT_CREATED_RESPONSE,
    OBJECT_DELETED_RESPONSE,
    OBJECT_MODIFIED_RESPONSE,
    OBJECT_NOT_FOUND_RESPONSE,
    OPINIONS_RESPONSE,
    OPINION_ALREADY_EXISTS_RESPONSE,
    BOOK_DOES_NOT_EXIST_RESPONSE,
    SORT_PARAM_DOES_NOT_EXIST,
)


class Opinion(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.post_parser.add_arg("book_id", type=str)
        self.post_parser.add_arg("stars_count", type=int_range_validation(min=1, max=5))
        self.post_parser.add_arg(
            "comment", type=string_range_validation(min=2, max=1000)
        )
        self.post_parser.add_arg("language", required=False)

        self.delete_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.delete_parser.add_arg("id", type=int)
        self.delete_parser.add_arg("language", required=False)

        self.patch_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.patch_parser.add_arg("id", type=int)
        self.patch_parser.add_arg(
            "stars_count", type=int_range_validation(min=1, max=5), required=False
        )
        self.patch_parser.add_arg(
            "comment", type=string_range_validation(min=2, max=1000), required=False
        )
        self.patch_parser.add_arg("language", required=False)
        super(Opinion, self).__init__()

    def get(self) -> Response:
        page: int = request.args.get("page", 1, type=int)
        per_page: int = request.args.get("per_page", 8, type=int)
        language: str = request.args.get("language", type=str)
        sorts: str = request.args.get("sorts", "modified_date", type=str)
        opinion_id: int = request.args.get("id", type=int)
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        opinion_query = opinion.Opinion.query
        if opinion_id:
            opinion_query = opinion_query.filter(opinion.Opinion.id == opinion_id)

        for sort in sorts.split(","):
            if sort.startswith("-"):
                try:
                    field = getattr(opinion.Opinion, sort[1:])
                except AttributeError:
                    return create_response(SORT_PARAM_DOES_NOT_EXIST, language=language)
                opinion_query = opinion_query.order_by(desc(field))
            else:
                try:
                    field = getattr(opinion.Opinion, sort)
                except AttributeError:
                    return create_response(SORT_PARAM_DOES_NOT_EXIST, language=language)
                opinion_query = opinion_query.order_by(field)

        opinion_objects = opinion_query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        return create_response(
            OPINIONS_RESPONSE,
            {
                "results": [
                    opinion_object.as_dict() for opinion_object in opinion_objects
                ],
                "pagination": {
                    "count": opinion_objects.total,
                    "page": page,
                    "pages": opinion_objects.pages,
                    "per_page": opinion_objects.per_page,
                },
            },
            language=language,
        )

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        book_id: str = args.get("book_id")
        stars_count: int = args.get("stars_count")
        comment: str = args.get("comment")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()

        existing_opinion: opinion.Opinion = opinion.Opinion.query.filter_by(
            user_id=user.id, book_id=book_id
        ).first()
        if existing_opinion:
            return create_response(OPINION_ALREADY_EXISTS_RESPONSE, language=language)
        existing_book: book.Book = book.Book.query.filter_by(id=book_id).first()
        if not existing_book:
            return create_response(BOOK_DOES_NOT_EXIST_RESPONSE, language=language)

        opinion_object: opinion.Opinion = opinion.Opinion(
            user_id=user.id,
            book_id=book_id,
            stars_count=stars_count,
            comment=comment,
        )
        db.session.add(opinion_object)
        db.session.commit()

        return create_response(
            OBJECT_CREATED_RESPONSE, opinion_object.as_dict(), language=language
        )

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        opinion_id: int = args.get("id")
        language: str = args.get("language")
        user_id: str = args.get("user_id")
        book_id: str = args.get("book_id")
        filters_list = [opinion.Opinion.id == opinion_id]
        if user_id:
            filters_list.append(opinion.Opinion.user_id == user_id)
        if book_id:
            filters_list.append(opinion.Opinion.book_id == book_id)
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user_object: User = User.query.filter_by(email=email).first()

        opinion_object: opinion.Opinion = opinion.Opinion.query.filter(
            *filters_list
        ).first()
        if not opinion_object:
            return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
        if not user_object.is_admin and user_object.id != opinion_object.user_id:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        existing_book: book.Book = book.Book.query.filter_by(
            id=opinion_object.book_id
        ).first()
        if not existing_book:
            return create_response(BOOK_DOES_NOT_EXIST_RESPONSE, language=language)

        score = (
            existing_book.score * existing_book.opinions_count
            - opinion_object.stars_count
        )
        existing_book.opinions_count -= 1
        if existing_book.opinions_count == 0:
            existing_book.score = 0
        else:
            existing_book.score = score / existing_book.opinions_count
        opinion_user = user.User.query.filter_by(id=opinion_object.user_id).first()
        opinion_user.opinions_count -= 1
        opinion_user.score -= 1
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
        if not user.is_admin and user.email != email:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        modified_opinion = opinion.Opinion.query.filter_by(id=opinion_id).first()

        if modified_opinion:
            if stars_count:
                existing_book: book.Book = book.Book.query.filter_by(
                    id=modified_opinion.book_id
                ).first()
                if not existing_book:
                    return create_response(
                        BOOK_DOES_NOT_EXIST_RESPONSE, language=language
                    )
                score = (
                    existing_book.score * existing_book.opinions_count
                    - modified_opinion.stars_count
                    + stars_count
                )
                existing_book.score = score / existing_book.opinions_count
                modified_opinion.stars_count = stars_count
                modified_opinion.modified_date = datetime.datetime.now()
            if comment:
                modified_opinion.comment = comment
                modified_opinion.modified_date = datetime.datetime.now()
            db.session.commit()
            return create_response(
                OBJECT_MODIFIED_RESPONSE, modified_opinion.as_dict(), language=language
            )
        return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
