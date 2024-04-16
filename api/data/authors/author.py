from flask import Response, request
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser
from helpers.request_response import create_response
from models import author, book
from models.user import User
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    INSUFFICIENT_PERMISSIONS_RESPONSE,
    OBJECT_MODIFIED_RESPONSE,
    OBJECT_DELETED_RESPONSE,
    OBJECT_CREATED_RESPONSE,
    AUTHORS_RESPONSE,
    PARAM_NOT_INT_RESPONSE,
    USER_DOES_NOT_EXIST_RESPONSE,
    FAN_DOES_NOT_EXIST_RESPONSE,
    AUTHOR_DOES_NOT_EXIST_RESPONSE,
    BOOK_DOES_NOT_EXIST_RESPONSE,
)


class Author(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("name")
        self.post_parser.add_arg("genres", type=list)
        self.post_parser.add_arg("biography")
        self.post_parser.add_arg("picture")
        self.post_parser.add_arg("fans", type=list, required=False)
        self.post_parser.add_arg("released_books", type=list, required=False)
        self.post_parser.add_arg("language", required=False)

        self.delete_parser: RequestParser = RequestParser()
        self.delete_parser.add_arg("id", type=int)
        self.delete_parser.add_arg("language", required=False)

        self.patch_parser: RequestParser = RequestParser()
        self.patch_parser.add_arg("id", type=int)
        self.patch_parser.add_arg("name", required=False)
        self.patch_parser.add_arg("genres", type=list, required=False)
        self.patch_parser.add_arg("biography", required=False)
        self.patch_parser.add_arg("picture", required=False)
        self.patch_parser.add_arg("language", required=False)

        super(Author, self).__init__()

    def get(self) -> Response:
        language: str = request.args.get("language")
        author_id: str = request.args.get("id")
        name: str = request.args.get("name")
        genres: list = request.args.getlist("genres")
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        if author_id:
            try:
                author_id: int = int(author_id)
            except ValueError:
                return create_response(PARAM_NOT_INT_RESPONSE, language=language)

        filters_list = []
        if genres:
            filters_list = [author.Author.genres.any(genres) for genres in genres]
        if name:
            filters_list.append(author.Author.name.ilike(f"%{name}%"))
        if author_id:
            filters_list.append(author.Author.id == author_id)

        author_objects: list[author.Author] = author.Author.query.filter(
            *filters_list
        ).all()

        return create_response(
            AUTHORS_RESPONSE,
            [author_object.as_dict() for author_object in author_objects]
            if len(author_objects) > 1
            else author_objects[0].as_dict()
            if len(author_objects) == 1
            else [],
            language=language,
            not_translated={"name", "picture"},
        )

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        name: str = args.get("name")
        genres: list[str] = args.get("genres")
        biography: str = args.get("biography")
        picture: str = args.get("picture")
        fans: list[int] = args.get("fans")
        released_books: list[int] = args.get("released_books")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        for fan in fans:
            if not User.query.filter_by(id=fan).first():
                return create_response(FAN_DOES_NOT_EXIST_RESPONSE, language=language)
        for released_book in released_books:
            if not book.Book.query.filter_by(id=released_book).first():
                return create_response(BOOK_DOES_NOT_EXIST_RESPONSE, language=language)
        author_object: author.Author = author.Author(
            name=name,
            genres=genres,
            biography=biography,
            picture=picture,
            fans=fans if fans else [],
            released_books=released_books if released_books else [],
        )
        db.session.add(author_object)
        db.session.commit()

        return create_response(OBJECT_CREATED_RESPONSE, language=language)

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        author_id: int = args.get("id")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        author_object: author.Author = author.Author.query.filter_by(
            id=author_id
        ).first()

        if not author_object:
            return create_response(AUTHOR_DOES_NOT_EXIST_RESPONSE, language=language)

        db.session.delete(author_object)
        db.session.commit()

        return create_response(OBJECT_DELETED_RESPONSE, language=language)

    def patch(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        author_id: int = args.get("id")
        name: str = args.get("name")
        genres: list[str] = args.get("genres")
        biography: str = args.get("biography")
        picture: str = args.get("picture")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if user:
            if not user.is_admin:
                return create_response(
                    INSUFFICIENT_PERMISSIONS_RESPONSE, language=language
                )
        else:
            return create_response(USER_DOES_NOT_EXIST_RESPONSE, language=language)

        modified_author: author.Author = author.Author.query.filter_by(
            id=author_id
        ).first()

        if user:
            if name:
                modified_author.name = name
            if genres:
                modified_author.genres = genres
            if biography:
                modified_author.biography = biography
            if picture:
                modified_author.picture = picture
            db.session.commit()

        return create_response(OBJECT_MODIFIED_RESPONSE, language=language)
