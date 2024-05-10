import datetime

from flask import Response, request
from flask_restful import Resource
from sqlalchemy import desc

from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import create_response
from models import book
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    BOOKS_RESPONSE,
    SORT_PARAM_DOES_NOT_EXIST,
)


class NewBook(Resource):
    def __init__(self) -> None:
        super(NewBook, self).__init__()

    def get(self) -> Response:
        page: int = request.args.get("page", 1, type=int)
        per_page: int = request.args.get("per_page", 8, type=int)
        sorts: str = request.args.get("sorts", "title", type=str)
        language: str = request.args.get("language", type=str)
        book_language: str = request.args.get("book_language", type=str)
        book_id: str = request.args.get("id", type=str)
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

        book_objects = book_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
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
