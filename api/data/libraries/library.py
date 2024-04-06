from flask import Response
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser, create_response
from models import library
from models.user import User
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    INSUFFICIENT_PERMISSIONS_RESPONSE,
    OBJECT_MODIFIED_RESPONSE,
    OBJECT_DELETED_RESPONSE,
    LIBRARY_OBJECT_RESPONSE,
    LIBRARY_OBJECTS_LIST_RESPONSE,
    OBJECT_NOT_FOUND_RESPONSE,
)


class Library(Resource):
    def __init__(self) -> None:
        self.get_parser: RequestParser = RequestParser()
        self.get_parser.add_arg("id", type=int, required=False)
        self.get_parser.add_arg("language", required=False)
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("read_books", type=list, required=False)
        self.post_parser.add_arg("bought_books", type=list, required=False)
        self.post_parser.add_arg("favourite_books", type=list, required=False)
        self.post_parser.add_arg("user_id", type=int)
        self.post_parser.add_arg("language", required=False)
        self.delete_parser: RequestParser = RequestParser()
        self.delete_parser.add_arg("id", type=int)
        self.delete_parser.add_arg("language", required=False)
        self.patch_parser: RequestParser = RequestParser()
        self.patch_parser.add_arg("id", type=int)
        self.patch_parser.add_arg("read_books", type=list, required=False)
        self.patch_parser.add_arg("bought_books", type=list, required=False)
        self.patch_parser.add_arg("favourite_books", type=list, required=False)
        self.patch_parser.add_arg("language", required=False)
        super(Library, self).__init__()

    def get(self) -> Response:
        args: dict = self.get_parser.parse_args()
        library_id: int = args.get("id")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if library_id:
            library_object: library.Library = library.Library.query.filter_by(
                id=library_id
            ).first()
            if not library_object:
                return create_response(OBJECT_NOT_FOUND_RESPONSE, language=language)
            if not user.is_admin:
                if not user.id == library_object.user_id:
                    return create_response(
                        INSUFFICIENT_PERMISSIONS_RESPONSE, language=language
                    )
            return create_response(
                LIBRARY_OBJECT_RESPONSE, library_object.as_dict(), language=language
            )
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)
        library_objects: list[library.Library] = library.Library.query.all()
        return create_response(
            LIBRARY_OBJECTS_LIST_RESPONSE,
            {
                "libraries": [
                    library_object.as_dict() for library_object in library_objects
                ]
            },
            language=language,
        )

    # TODO Do rozważenia post na library bo ono zawsze jest tworzone przy tworzeniu usera

    # def post(self) -> Response:
    #     args: dict = self.post_parser.parse_args()
    #     read_books: list[int] = args.get("read_books")
    #     bought_books: list[int] = args.get("bought_books")
    #     favourite_books: list[int] = args.get("favourite_books")
    #     user_id: int = args.get("user_id")
    #     email: str | None = verify_jwt_token()
    #     if not email:
    #         return create_response(TOKEN_INVALID_RESPONSE, language=language)
    #     user: User = User.query.filter_by(email=email).first()
    #     if not user.is_admin:
    #         return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)
    #     # TODO A CO JEŚLI USER O TAKIM ID NIE ISTNIEJE?
    #     library_object: library.Library = library.Library(
    #         read_books=read_books if read_books else [],
    #         bought_books=bought_books if bought_books else [],
    #         favourite_books=favourite_books if favourite_books else [],
    #         user_id=user_id,
    #     )
    #     db.session.add(library_object)
    #     db.session.commit()
    #
    #     return create_response(OBJECT_CREATED_RESPONSE, language=language)

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        library_id: int = args.get("id")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        library_object: library.Library = library.Library.query.filter_by(
            id=library_id
        ).first()

        db.session.delete(library_object)
        db.session.commit()

        return create_response(OBJECT_DELETED_RESPONSE, language=language)

    def patch(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        library_id: int = args.get("id")
        read_books: list[int] = args.get("read_books")
        bought_books: list[int] = args.get("bought_books")
        favourite_books: list[int] = args.get("favourite_books")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        modified_library: library.Library = library.Library.query.filter_by(
            id=library_id
        ).first()

        if user:
            if read_books:
                modified_library.read_books = read_books
            if bought_books:
                modified_library.bought_books = bought_books
            if favourite_books:
                modified_library.favourite_books = favourite_books
            db.session.commit()

        return create_response(OBJECT_MODIFIED_RESPONSE, language=language)
