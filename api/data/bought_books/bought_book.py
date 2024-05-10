from flask import Response, request
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser, create_response, APIArgument

from models import book, library, user
from static.responses import (
    USER_NOT_FOUND_RESPONSE,
    BOOK_NOT_FOUND_RESPONSE,
    OBJECT_CREATED_RESPONSE,
    BOOKS_RESPONSE,
    TOKEN_INVALID_RESPONSE,
    BOOK_ALREADY_IN_BOUGHT_BOOKS_RESPONSE,
    BOOK_NOT_IN_BOUGHT_BOOKS_RESPONSE,
    LIBRARY_NOT_FOUND_RESPONSE,
    OBJECT_REMOVED_RESPONSE,
)


class BoughtBook(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.post_parser.add_arg("language", required=False)
        self.post_parser.add_arg("user_id", type=int, required=False)
        self.post_parser.add_arg("book_id", type=str)

        self.delete_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.delete_parser.add_arg("language", required=False)
        self.delete_parser.add_arg("user_id", type=int, required=False)
        self.delete_parser.add_arg("user_id", type=int)
        super(BoughtBook, self).__init__()

    def get(self) -> Response:
        page: int = request.args.get("page", 1, type=int)
        per_page: int = request.args.get("per_page", 8, type=int)
        language: str = request.args.get("language")
        user_id: int = request.args.get("user_id", type=int)
        book_id: str = request.args.get("book_id", type=str)
        email = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        library_query = library.Library.query
        book_query = book.Book.query
        if user_id:
            library_query = library_query.filter_by(user_id=user_id)
        else:
            current_user_id = user.User.query.filter_by(email=email).first().id
            library_query = library_query.filter_by(user_id=current_user_id)
        if book_id:
            book_query = book_query.filter_by(id=book_id)

        library_object: library.Library = library_query.first()
        if not library_object:
            return create_response(LIBRARY_NOT_FOUND_RESPONSE, language=language)
        bought_book_ids = [
            bought_book.id for bought_book in library_object.bought_books
        ]
        book_query = book_query.filter(book.Book.id.in_(bought_book_ids))
        book_objects = book_query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        if library_object:
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
        return create_response(USER_NOT_FOUND_RESPONSE, language=language)

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        language: str = args.get("language")
        user_id: int = args.get("user_id")
        book_id: str = args.get("book_id")
        email = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        library_query = library.Library.query
        book_query = book.Book.query
        if user_id:
            library_query = library_query.filter_by(user_id=user_id)
        else:
            current_user_id = user.User.query.filter_by(email=email).first().id
            library_query = library_query.filter_by(user_id=current_user_id)
        book_query = book_query.filter_by(id=book_id)

        library_object: library.Library = library_query.first()
        book_object = book_query.first()

        if library_object and book_object:
            if book_object not in library_object.bought_books:
                library_object.bought_books.append(book_object)
                library_object.bought_books_count += 1
                db.session.commit()
                return create_response(
                    OBJECT_CREATED_RESPONSE, library_object.as_dict(), language=language
                )
            else:
                return create_response(
                    BOOK_ALREADY_IN_BOUGHT_BOOKS_RESPONSE, language=language
                )
        elif not library_object:
            return create_response(USER_NOT_FOUND_RESPONSE, language=language)
        return create_response(BOOK_NOT_FOUND_RESPONSE, language=language)

    def delete(self) -> Response:
        args: dict = self.post_parser.parse_args()
        language: str = args.get("language")
        user_id: int = args.get("user_id")
        book_id: str = args.get("book_id")
        email = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        if user_id:
            library_query = library.Library.query.filter_by(user_id=user_id)
        else:
            current_user_id = user.User.query.filter_by(email=email).first().id
            library_query = library.Library.query.filter_by(user_id=current_user_id)
        book_query = book.Book.query.filter_by(id=book_id)

        library_object: library.Library = library_query.first()
        book_object: book.Book = book_query.first()

        if library_object and book_object:
            if book_object in library_object.bought_books:
                library_object.bought_books.remove(book_object)
                library_object.bought_books_count -= 1
                db.session.commit()
                return create_response(
                    OBJECT_REMOVED_RESPONSE, library_object.as_dict(), language=language
                )
            else:
                return create_response(
                    BOOK_NOT_IN_BOUGHT_BOOKS_RESPONSE, language=language
                )
        elif not library_object:
            return create_response(USER_NOT_FOUND_RESPONSE, language=language)
        return create_response(BOOK_NOT_FOUND_RESPONSE, language=language)
