from flask import Response, request
from flask_restful import Resource
from sqlalchemy import desc

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser, string_range_validation, APIArgument
from helpers.request_response import create_response
from models import author
from models.user import User
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    INSUFFICIENT_PERMISSIONS_RESPONSE,
    OBJECT_MODIFIED_RESPONSE,
    OBJECT_DELETED_RESPONSE,
    OBJECT_CREATED_RESPONSE,
    AUTHORS_RESPONSE,
    USER_DOES_NOT_EXIST_RESPONSE,
    AUTHOR_DOES_NOT_EXIST_RESPONSE,
    SORT_PARAM_DOES_NOT_EXIST,
)


class Author(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.post_parser.add_arg("name", type=string_range_validation(max=200))
        self.post_parser.add_arg("biography", type=string_range_validation(max=3000))
        self.post_parser.add_arg("picture", type=string_range_validation(max=200))
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
        self.patch_parser.add_arg(
            "name", type=string_range_validation(max=200), required=False
        )
        self.patch_parser.add_arg(
            "biography", type=string_range_validation(max=3000), required=False
        )
        self.patch_parser.add_arg(
            "picture", type=string_range_validation(max=200), required=False
        )
        self.patch_parser.add_arg("language", required=False)

        super(Author, self).__init__()

    def get(self) -> Response:
        page: int = request.args.get("page", 1, type=int)
        per_page: int = request.args.get("per_page", 8, type=int)
        sorts: str = request.args.get("sorts", "name", type=str)
        language: str = request.args.get("language", type=str)
        author_id: int = request.args.get("id", type=int)
        name: str = request.args.get("name", type=str)
        name_is_startswith: bool = request.args.get(
            "name_is_startswith", False, type=bool
        )
        genres: list[str] = request.args.getlist("genres", type=str)
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        author_query = author.Author.query
        if genres:
            author_query = author_query.filter(
                *[author.Author.genres.any(genres) for genres in genres]
            )
        print(name_is_startswith)
        if name:
            if name_is_startswith:
                print("BBB")
                author_query = author_query.filter(author.Author.name.ilike(f"{name}%"))
            else:
                print(name_is_startswith)
                print("AAAA")
                author_query = author_query.filter(
                    author.Author.name.ilike(f"%{name}%")
                )
        if author_id:
            author_query = author_query.filter(author.Author.id == author_id)

        for sort in sorts.split(","):
            if sort.startswith("-"):
                try:
                    field = getattr(author.Author, sort[1:])
                except AttributeError:
                    return create_response(SORT_PARAM_DOES_NOT_EXIST, language=language)
                author_query = author_query.order_by(desc(field))
            else:
                try:
                    field = getattr(author.Author, sort)
                except AttributeError:
                    return create_response(SORT_PARAM_DOES_NOT_EXIST, language=language)
                author_query = author_query.order_by(field)

        author_objects = author_query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        return create_response(
            AUTHORS_RESPONSE,
            {
                "results": [
                    author_object.as_dict() for author_object in author_objects
                ],
                "pagination": {
                    "count": author_objects.total,
                    "page": page,
                    "pages": author_objects.pages,
                    "per_page": author_objects.per_page,
                },
            },
            language=language,
            not_translated={"name", "picture"},
        )

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        name: str = args.get("name")
        biography: str = args.get("biography")
        picture: str = args.get("picture")
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE, language=language)

        author_object: author.Author = author.Author(
            name=name,
            biography=biography,
            picture=picture,
        )
        db.session.add(author_object)
        db.session.commit()

        return create_response(
            OBJECT_CREATED_RESPONSE, author_object.as_dict(), language=language
        )

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
            if biography:
                modified_author.biography = biography
            if picture:
                modified_author.picture = picture
            db.session.commit()

        return create_response(
            OBJECT_MODIFIED_RESPONSE, modified_author.as_dict(), language=language
        )
