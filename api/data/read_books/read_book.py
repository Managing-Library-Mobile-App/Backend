from flask import Response, request
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser, create_response, APIArgument

from models import book, library
from static.responses import (
    OBJECT_DELETED_RESPONSE,
    USER_NOT_FOUND_RESPONSE,
    BOOK_NOT_FOUND_RESPONSE,
    BOOK_NOT_IN_READ_BOOKS_RESPONSE,
    OBJECT_CREATED_RESPONSE,
    BOOKS_RESPONSE,
    BOOK_ALREADY_IN_READ_BOOKS_RESPONSE,
    USER_ID_NOT_PROVIDED_RESPONSE,
    TOKEN_INVALID_RESPONSE,
    LIBRARY_NOT_FOUND_RESPONSE,
)


class ReadBook(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.post_parser.add_arg("language", required=False)
        self.post_parser.add_arg("user_id", type=int)
        self.post_parser.add_arg("book_id", type=int)

        self.delete_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.delete_parser.add_arg("language", required=False)
        self.delete_parser.add_arg("user_id", type=int)
        self.delete_parser.add_arg("book_id", type=int)
        super(ReadBook, self).__init__()

    def get(self) -> Response:
        page: int = request.args.get("page", 1, type=int)
        per_page: int = request.args.get("per_page", 8, type=int)
        language: str = request.args.get("language")
        user_id: int = request.args.get("user_id", type=int)
        book_id: int = request.args.get("book_id", type=int)
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        library_query = library.Library.query
        book_query = book.Book.query
        if user_id:
            library_query = library_query.filter_by(user_id=user_id)
        else:
            return create_response(USER_ID_NOT_PROVIDED_RESPONSE, language=language)
        if book_id:
            book_query = book_query.filter_by(id=book_id)

        library_object: library.Library = library_query.first()
        if library_object:
            return create_response(LIBRARY_NOT_FOUND_RESPONSE, language=language)
        read_book_ids = [read_book.id for read_book in library_object.read_books]
        book_query = book_query.filter(book.Book.id.in_(read_book_ids))
        book_objects = book_query.paginate(page=page, per_page=per_page)

        if library_object and book_objects:
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
            )
        elif not library_object:
            return create_response(USER_NOT_FOUND_RESPONSE, language=language)
        return create_response(BOOK_NOT_FOUND_RESPONSE, language=language)

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        language: str = args.get("language")
        user_id: int = args.get("user_id")
        book_id: int = args.get("book_id")
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        library_query = library.Library.query
        book_query = book.Book.query
        library_query = library_query.filter_by(user_id=user_id)
        book_query = book_query.filter_by(id=book_id)

        library_object: library.Library = library_query.first()
        book_object = book_query.first()

        if library_object and book_object:
            if book_object not in library_object.read_books:
                library_object.read_books.append(book_object)
                db.session.commit()
                return create_response(OBJECT_CREATED_RESPONSE, language=language)
            else:
                return create_response(
                    BOOK_ALREADY_IN_READ_BOOKS_RESPONSE, language=language
                )
        elif not library_object:
            return create_response(USER_NOT_FOUND_RESPONSE, language=language)
        return create_response(BOOK_NOT_FOUND_RESPONSE, language=language)

    def delete(self) -> Response:
        args: dict = self.post_parser.parse_args()
        language: str = args.get("language")
        user_id: int = args.get("user_id")
        book_id: int = args.get("book_id")
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        library_query = library.Library.query.filter_by(user_id=user_id)
        book_query = book.Book.query.filter_by(id=book_id)

        library_object: library.Library = library_query.first()
        book_object: book.Book = book_query.first()

        if library_object:
            if book_object in library_object.read_books:
                library_object.read_books.remove(book_object)
                db.session.commit()
                return create_response(OBJECT_DELETED_RESPONSE, language=language)
            else:
                return create_response(
                    BOOK_NOT_IN_READ_BOOKS_RESPONSE, language=language
                )
        return create_response(USER_NOT_FOUND_RESPONSE, language=language)
