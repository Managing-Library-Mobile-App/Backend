import datetime

from flask import Response, request
from flask_restful import Resource
from sqlalchemy import desc

from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser, APIArgument
from helpers.request_response import create_response
from models import book
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    BOOKS_RESPONSE,
    SORT_PARAM_DOES_NOT_EXIST,
)


class NewBook(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.post_parser.add_arg("isbn", type=int)
        self.post_parser.add_arg("title")
        self.post_parser.add_arg("author_id")
        self.post_parser.add_arg("publishing_house")
        self.post_parser.add_arg("description")
        self.post_parser.add_arg("genres", type=list)
        self.post_parser.add_arg("picture")
        self.post_parser.add_arg("premiere_date")
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
        self.patch_parser.add_arg("isbn")
        self.patch_parser.add_arg("title")
        self.patch_parser.add_arg("author_id")
        self.patch_parser.add_arg("publishing_house")
        self.patch_parser.add_arg("description")
        self.patch_parser.add_arg("genres", type=list)
        self.patch_parser.add_arg("picture")
        self.patch_parser.add_arg("premiere_date")
        self.patch_parser.add_arg("language", required=False)
        super(NewBook, self).__init__()

    def get(self) -> Response:
        page: int = request.args.get("page", 1, type=int)
        per_page: int = request.args.get("per_page", 8, type=int)
        sorts: str = request.args.get("sort", "title", type=str)
        language: str = request.args.get("language", type=str)
        book_language: str = request.args.get("book_language", type=str)
        book_id: int = request.args.get("id", type=int)
        genres: list[str] = request.args.getlist("genres", type=str)
        title: str = request.args.get("title", type=str)
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        book_query = book.Book.query
        book_query = book_query.filter(
            book.Book.premiere_date
            >= datetime.datetime.now() - datetime.timedelta(days=90)
        )
        if genres:
            book_query = book_query.filter(
                *[book.Book.genres.any(genres) for genres in genres]
            )
        if title:
            book_query = book_query.filter(book.Book.title.ilike(f"%{title}%"))
        if book_id:
            book_query = book_query.filter(book.Book.id == book_id)
        if book_language:
            book_query = book_query.filter(book.Book.language == book_language)

        for sort in sorts.split(","):
            if sort.startswith("-"):
                try:
                    field = getattr(book.Book, sort[1:])
                except AttributeError:
                    return create_response(SORT_PARAM_DOES_NOT_EXIST, language=language)
                book_query = book_query.order_by(desc(field))
            else:
                try:
                    field = getattr(book.Book, sort)
                except AttributeError:
                    return create_response(SORT_PARAM_DOES_NOT_EXIST, language=language)
                book_query = book_query.order_by(field)

        book_objects = book_query.paginate(page=page, per_page=per_page)
        return create_response(
            BOOKS_RESPONSE,
            {
                "results": [book_object.as_dict() for book_object in book_objects],
                "pagination": {
                    "count": book_objects.total,
                    "page": page,
                    "pages": book_objects.pages,
                    "per_page": book_objects.per_page,
                },
            },
            language=language,
            not_translated={"isbn", "title", "publishing_house", "picture"},
        )
