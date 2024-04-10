import datetime

from flask import Response, request
from flask_restful import Resource
from sqlalchemy import and_

from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser
from helpers.request_response import create_response
from models import book
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    BOOK_OBJECT_RESPONSE,
    BOOK_OBJECTS_LIST_RESPONSE,
    OBJECT_NOT_FOUND_RESPONSE,
)


class NewBook(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("isbn", type=int)
        self.post_parser.add_arg("title")
        self.post_parser.add_arg("author_id")
        self.post_parser.add_arg("publishing_house")
        self.post_parser.add_arg("description")
        self.post_parser.add_arg("genres", type=list)
        self.post_parser.add_arg("picture")
        self.post_parser.add_arg("premiere_date")
        self.post_parser.add_arg("language", required=False)
        self.delete_parser: RequestParser = RequestParser()
        self.delete_parser.add_arg("id", type=int)
        self.delete_parser.add_arg("language", required=False)
        self.patch_parser: RequestParser = RequestParser()
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
        language: str = request.args.get("language")
        book_id: str = request.args.get("id")
        if book_id:
            try:
                book_id: int = int(book_id)
            except ValueError:
                return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
        not_translated: set[str] = {"isbn", "title", "publishing_house", "picture"}
        genres: list = request.args.getlist("genres")
        filters_list = []
        if genres:
            filters_list = [book.Book.genres.any(genres) for genres in genres]

        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        if book_id:
            book_object: book.Book = book.Book.query.filter(
                and_(
                    book.Book.id == book_id,
                    book.Book.premiere_date
                    >= datetime.datetime.now() - datetime.timedelta(days=90),
                    *filters_list,
                )
            ).first()

            if not book_object:
                return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
            return create_response(
                BOOK_OBJECT_RESPONSE,
                book_object.as_dict(),
                language=language,
                not_translated=not_translated,
            )
        book_objects: list[book.Book] = book.Book.query.filter(
            and_(
                book.Book.premiere_date
                >= datetime.datetime.now() - datetime.timedelta(days=90),
                *filters_list,
            )
        ).all()
        return create_response(
            BOOK_OBJECTS_LIST_RESPONSE,
            {"books": [book_object.as_dict() for book_object in book_objects]},
            language=language,
            not_translated=not_translated,
        )
