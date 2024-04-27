from flask import Response, request
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser, create_response, APIArgument
from models import library
from models.user import User
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    INSUFFICIENT_PERMISSIONS_RESPONSE,
    OBJECT_MODIFIED_RESPONSE,
    LIBRARIES_RESPONSE,
)


class Library(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.post_parser.add_arg("read_books", type=list, required=False)
        self.post_parser.add_arg("bought_books", type=list, required=False)
        self.post_parser.add_arg("favourite_books", type=list, required=False)
        self.post_parser.add_arg("user_id", type=int)
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
        self.patch_parser.add_arg("read_books", type=list, required=False)
        self.patch_parser.add_arg("bought_books", type=list, required=False)
        self.patch_parser.add_arg("favourite_books", type=list, required=False)
        self.patch_parser.add_arg("language", required=False)
        super(Library, self).__init__()

    def get(self) -> Response:
        page: int = request.args.get("page", 1, type=int)
        per_page: int = request.args.get("per_page", 8, type=int)
        language: str = request.args.get("language", type=str)
        library_id: int = request.args.get("id", type=int)
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        library_query = library.Library.query
        if library_id:
            library_query = library_query.filter(library.Library.id == library_id)

        library_objects = library_query.paginate(page=page, per_page=per_page)

        return create_response(
            LIBRARIES_RESPONSE,
            {
                "results": [
                    library_object.as_dict() for library_object in library_objects
                ],
                "pagination": {
                    "count": library_objects.total,
                    "page": page,
                    "pages": library_objects.pages,
                    "per_page": library_objects.per_page,
                },
            },
            language=language,
        )

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
