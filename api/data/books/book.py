import datetime
import uuid

from flask import Response, request
from flask_restful import Resource
from sqlalchemy import desc

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser, string_range_validation, APIArgument
from helpers.request_response import create_response
from models import book, author
from models.user import User
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    INSUFFICIENT_PERMISSIONS_RESPONSE,
    OBJECT_MODIFIED_RESPONSE,
    OBJECT_DELETED_RESPONSE,
    OBJECT_CREATED_RESPONSE,
    BOOKS_RESPONSE,
    OBJECT_NOT_FOUND_RESPONSE,
    WRONG_DATE_FORMAT_RESPONSE,
    SORT_PARAM_DOES_NOT_EXIST,
    AUTHOR_NOT_FOUND_RESPONSE,
    ID_MISSING_RESPONSE,
)


class Book(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.post_parser.add_arg("book_language", type=string_range_validation(max=50))
        self.post_parser.add_arg("isbn", type=string_range_validation(max=1000))
        self.post_parser.add_arg("title", type=string_range_validation(max=200))
        self.post_parser.add_arg("authors", type=list)
        self.post_parser.add_arg(
            "publishing_house", type=string_range_validation(max=200)
        )
        self.post_parser.add_arg("description", type=string_range_validation(max=15000))
        self.post_parser.add_arg("genres", type=list)
        self.post_parser.add_arg("picture", type=string_range_validation(max=200))
        self.post_parser.add_arg("premiere_date")
        self.post_parser.add_arg("language", required=False)

        self.delete_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.delete_parser.add_arg("id", type=str)
        self.delete_parser.add_arg("language", required=False)

        self.patch_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.patch_parser.add_arg("book_language")
        self.patch_parser.add_arg("id", type=str)
        self.patch_parser.add_arg("isbn", type=string_range_validation(max=1000))
        self.patch_parser.add_arg("title", type=string_range_validation(max=200))
        self.patch_parser.add_arg(
            "publishing_house", type=string_range_validation(max=200)
        )
        self.patch_parser.add_arg(
            "description", type=string_range_validation(max=15000)
        )
        self.patch_parser.add_arg("picture", type=string_range_validation(max=200))
        self.patch_parser.add_arg("premiere_date")
        self.patch_parser.add_arg("language", required=False)
        super(Book, self).__init__()

    def get(self) -> Response:
        page: int = request.args.get("page", 1, type=int)
        per_page: int = request.args.get("per_page", 8, type=int)
        sorts: str = request.args.get("sorts", "title", type=str)
        language: str = request.args.get("language", type=str)
        id: str = request.args.get("id", type=str)
        title: str = request.args.get("title", type=str)
        authors: list[str] = request.args.getlist("authors", type=str)
        date_from: str | datetime.date = request.args.get("date_from", type=str)
        date_to: str | datetime.date = request.args.get("date_to", type=str)
        minimum_score: int = request.args.get("minimum_score", type=int)
        genres: list[str] = request.args.getlist("genres", type=str)
        book_language: str = request.args.get("book_language", type=str)
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        if date_from:
            try:
                date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").date()
            except ValueError:
                return create_response(WRONG_DATE_FORMAT_RESPONSE, language=language)
        if date_to:
            try:
                date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").date()
            except ValueError:
                return create_response(WRONG_DATE_FORMAT_RESPONSE, language=language)

        book_query = book.Book.query
        if genres:
            book_query = book_query.filter(
                *[book.Book.genres.any(genre) for genre in genres]
            )
        if title:
            book_query = book_query.filter(book.Book.title.ilike(f"%{title}%"))
        if authors:
            book_query = book_query.filter(
                *[book.Book.authors.any(author_id) for author_id in authors]
            )
        if date_from:
            book_query = book_query.filter(book.Book.premiere_date >= date_from)
        if date_to:
            book_query = book_query.filter(book.Book.premiere_date <= date_to)
        if minimum_score:
            book_query = book_query.filter(book.Book.score >= minimum_score)
        if id:
            book_query = book_query.filter(book.Book.id == id)
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

    def post(self) -> Response:
        id = str(uuid.uuid4())
        args: dict = self.post_parser.parse_args()
        isbn: str = args.get("isbn")
        title: str = args.get("title")
        authors: list[str] = args.get("authors")
        publishing_house: str = args.get("publishing_house")
        description: str = args.get("description")
        genres: list[str] = args.get("genres")
        picture: str = args.get("picture")
        premiere_date: datetime.datetime = args.get("premiere_date")
        language: str = args.get("language")
        book_language: str = args.get("book_language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)
        author_objects = author.Author.query.filter(
            *[author.Author.id == author_object_id for author_object_id in authors]
        ).all()
        if not author_objects:
            return create_response(AUTHOR_NOT_FOUND_RESPONSE, language=language)

        if not id:
            return create_response(ID_MISSING_RESPONSE, language=language)

        book_object: book.Book = book.Book(
            id=id,
            language=book_language,
            isbn=isbn,
            title=title,
            authors=authors,
            publishing_house=publishing_house,
            description=description,
            genres=genres,
            picture=picture,
            premiere_date=premiere_date,
        )
        db.session.add(book_object)
        db.session.commit()

        for author_object in author_objects:
            author_genres = set(author_object.genres)
            for genre in book_object.genres:
                author_genres.add(genre)
            author_object.genres = author_genres
        db.session.commit()

        return create_response(
            OBJECT_CREATED_RESPONSE, book_object.as_dict(), language=language
        )

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        book_id: str = args.get("id")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        book_object: book.Book = book.Book.query.filter_by(id=book_id).first()
        if not book_object:
            return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
        author_objects = author.Author.query.filter(
            *[
                author.Author.id == author_object.id
                for author_object in book_object.authors
            ]
        ).all()
        db.session.delete(book_object)
        db.session.commit()

        for author_object in author_objects:
            author_genres = set()
            for author_book in author_object.released_books:
                for genre in author_book.genres:
                    author_genres.add(genre)
            author_object.genres = author_genres
        db.session.commit()

        return create_response(OBJECT_DELETED_RESPONSE, language=language)

    def patch(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        book_id: str = args.get("id")
        isbn: str = args.get("isbn")
        title: str = args.get("title")
        publishing_house: str = args.get("publishing_house")
        description: str = args.get("description")
        picture: str = args.get("picture")
        premiere_date: datetime.datetime = args.get("premiere_date")
        language: str = args.get("language")
        book_language: str = args.get("book_language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        modified_book: book.Book = book.Book.query.filter_by(id=book_id).first()
        if user:
            if modified_book:
                if isbn:
                    modified_book.isbn = isbn
                if title:
                    modified_book.title = title
                if publishing_house:
                    modified_book.publishing_house = publishing_house
                if description:
                    modified_book.description = description
                if picture:
                    modified_book.picture = picture
                if premiere_date:
                    modified_book.premiere_date = premiere_date
                if book_language:
                    modified_book.book_language = book_language
                db.session.commit()
                return create_response(
                    OBJECT_MODIFIED_RESPONSE, modified_book.as_dict(), language=language
                )
        return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
