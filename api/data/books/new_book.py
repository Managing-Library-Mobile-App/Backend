import datetime

from flask import Response, request
from flask_restful import Resource

from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser
from helpers.request_response import create_response
from models import book
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    BOOKS_RESPONSE,
    PARAM_NOT_INT_RESPONSE,
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
        genres: list = request.args.getlist("genres")
        title: str = request.args.get("title")
        if not verify_jwt_token:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        if book_id:
            try:
                book_id: int = int(book_id)
            except ValueError:
                return create_response(PARAM_NOT_INT_RESPONSE, language=language)

        filters_list = [
            book.Book.premiere_date
            >= datetime.datetime.now() - datetime.timedelta(days=90),
        ]
        if genres:
            filters_list.extend([book.Book.genres.any(genres) for genres in genres])
        if title:
            filters_list.append(book.Book.title.ilike(f"%{title}%"))
        if book_id:
            filters_list.append(book.Book.id == book_id)

        book_objects: list[book.Book] = book.Book.query.filter(
            *filters_list,
        ).all()
        return create_response(
            BOOKS_RESPONSE,
            [book_object.as_dict() for book_object in book_objects]
            if len(book_objects) > 1
            else book_objects[0].as_dict()
            if len(book_objects) == 1
            else [],
            language=language,
            not_translated={"isbn", "title", "publishing_house", "picture"},
        )
