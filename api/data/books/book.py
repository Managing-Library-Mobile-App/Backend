import datetime

from flask import Response, request
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser
from helpers.request_response import create_response
from models import book
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
    PARAM_NOT_INT_RESPONSE,
)


class Book(Resource):
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
        super(Book, self).__init__()

    def get(self) -> Response:
        language: str = request.args.get("language")
        id: str = request.args.get("id")
        title: str = request.args.get("title")
        author_id: str = request.args.get("author_id")
        date_from: str | datetime.date = request.args.get("date_from")
        date_to: str | datetime.date = request.args.get("date_to")
        minimum_score: str | int = request.args.get("minimum_score")
        genres: list = request.args.getlist("genres")
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        if author_id:
            try:
                author_id: int = int(author_id)
            except ValueError:
                return create_response(PARAM_NOT_INT_RESPONSE, language=language)
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
        if minimum_score:
            try:
                minimum_score: int = int(minimum_score)
            except ValueError:
                return create_response(PARAM_NOT_INT_RESPONSE, language=language)

        filters_list = []
        if genres:
            filters_list.extend([book.Book.genres.any(genres) for genres in genres])
        if title:
            filters_list.append(book.Book.title.contains(title))
        if author_id:
            filters_list.append(book.Book.author_id == author_id)
        if date_from:
            filters_list.append(book.Book.premiere_date >= date_from)
        if date_to:
            filters_list.append(book.Book.premiere_date <= date_to)
        if minimum_score:
            filters_list.append(book.Book.score >= minimum_score)
        if id:
            filters_list.append(book.Book.id == id)

        book_objects: list[book.Book] = book.Book.query.filter(*filters_list).all()
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

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        isbn: str = args.get("isbn")
        title: str = args.get("title")
        author_id: int = args.get("author_id")
        publishing_house: str = args.get("publishing_house")
        description: str = args.get("description")
        genres: list[int] = args.get("genres")
        picture: str = args.get("picture")
        premiere_date: datetime.datetime = args.get("premiere_date")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        # TODO A CO JEŚLI AUTOR O TAKIM ID NIE ISTNIEJE?
        book_object: book.Book = book.Book(
            isbn=isbn,
            title=title,
            author_id=author_id,
            publishing_house=publishing_house,
            description=description,
            genres=genres,
            picture=picture,
            premiere_date=premiere_date,
        )
        db.session.add(book_object)
        db.session.commit()

        return create_response(OBJECT_CREATED_RESPONSE, language=language)

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        book_id: int = args.get("id")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        opinion_object: book.Book = book.Book.query.filter_by(id=book_id).first()
        if not opinion_object:
            return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
        db.session.delete(opinion_object)
        db.session.commit()

        return create_response(OBJECT_DELETED_RESPONSE, language=language)

    def patch(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        book_id: int = args.get("id")
        isbn: str = args.get("isbn")
        title: str = args.get("title")
        publishing_house: str = args.get("publishing_house")
        description: str = args.get("description")
        genres: list[int] = args.get("genres")
        picture: str = args.get("picture")
        premiere_date: datetime.datetime = args.get("premiere_date")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        modified_book: book.Book = book.Book.query.filter_by(id=book_id).first()

        if user:
            if isbn:
                modified_book.isbn = isbn
            if title:
                modified_book.title = title
            if publishing_house:
                modified_book.publishing_house = publishing_house
            if description:
                modified_book.description = description
            if genres:
                modified_book.genres = genres
            if picture:
                modified_book.picture = picture
            if premiere_date:
                modified_book.premiere_date = premiere_date
            db.session.commit()

        return create_response(OBJECT_MODIFIED_RESPONSE, language=language)
