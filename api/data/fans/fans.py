from flask import Response, request
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser, create_response, APIArgument

from models import user, author
from static.responses import (
    USER_NOT_FOUND_RESPONSE,
    OBJECT_CREATED_RESPONSE,
    TOKEN_INVALID_RESPONSE,
    USERS_RESPONSE,
    AUTHOR_NOT_FOUND_RESPONSE,
    USER_ALREADY_IN_FANS_RESPONSE,
    USER_NOT_IN_FANS_RESPONSE,
    OBJECT_REMOVED_RESPONSE,
    AUTHORS_RESPONSE,
)


class Fan(Resource):
    def __init__(self) -> None:
        self.post_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.post_parser.add_arg("language", required=False)
        self.post_parser.add_arg("user_id", type=int)
        self.post_parser.add_arg("author_id", type=int)

        self.delete_parser: RequestParser = RequestParser(
            argument_class=APIArgument, bundle_errors=True
        )
        self.delete_parser.add_arg("language", required=False)
        self.delete_parser.add_arg("user_id", type=int)
        self.delete_parser.add_arg("author_id", type=int)
        super(Fan, self).__init__()

    def get(self) -> Response:
        page: int = request.args.get("page", 1, type=int)
        per_page: int = request.args.get("per_page", 8, type=int)
        language: str = request.args.get("language")
        user_id: int = request.args.get("user_id", type=int)
        author_id: int = request.args.get("author_id", type=int)
        email = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        user_query = user.User.query
        author_query = author.Author.query
        if user_id:
            if user_id and not author_id:
                user_object: user.User = user_query.filter_by(id=user_id).first()
                followed_authors_ids = [
                    followed_author.id
                    for followed_author in user_object.followed_authors
                ]
                author_query = author_query.filter(
                    author.Author.id.in_(followed_authors_ids)
                )
                author_objects = author_query.paginate(
                    page=page, per_page=per_page, error_out=False
                )

                if author_query:
                    return create_response(
                        AUTHORS_RESPONSE,
                        {
                            "results": [
                                author_object.as_dict()
                                for author_object in author_objects
                            ],
                            "pagination": {
                                "count": author_objects.total,
                                "page": page,
                                "pages": author_objects.pages,
                                "per_page": author_objects.per_page,
                            },
                        },
                        language=language,
                    )
                return create_response(AUTHOR_NOT_FOUND_RESPONSE, language=language)

            user_query = user_query.filter_by(id=user_id)
        if author_id:
            author_query = author_query.filter_by(id=author_id)
        if not user_id and not author_id:
            user_object: user.User = user_query.filter_by(email=email).first()
            followed_authors_ids = [
                followed_author.id for followed_author in user_object.followed_authors
            ]
            author_query = author_query.filter(
                author.Author.id.in_(followed_authors_ids)
            )
            author_objects = author_query.paginate(
                page=page, per_page=per_page, error_out=False
            )

            if author_query:
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
                )
            return create_response(AUTHOR_NOT_FOUND_RESPONSE, language=language)

        author_query = author_query.first()
        if not author_query:
            return create_response(AUTHOR_NOT_FOUND_RESPONSE, language=language)
        fans_ids = [fan.id for fan in author_query.fans]
        user_query = user_query.filter(user.User.id.in_(fans_ids))
        user_objects = user_query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        if author_query:
            return create_response(
                USERS_RESPONSE,
                {
                    "results": [user_object.as_dict() for user_object in user_objects],
                    "pagination": {
                        "count": user_objects.total,
                        "page": page,
                        "pages": user_objects.pages,
                        "per_page": user_objects.per_page,
                    },
                },
                language=language,
            )
        return create_response(AUTHOR_NOT_FOUND_RESPONSE, language=language)

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        language: str = args.get("language")
        user_id: int = args.get("user_id")
        author_id: int = args.get("author_id")
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        user_query = user.User.query
        author_query = author.Author.query
        user_query = user_query.filter_by(id=user_id)
        author_query = author_query.filter_by(id=author_id)

        author_object: author.Author = author_query.first()
        user_object = user_query.first()

        if author_query:
            if user_object not in author_query.fans:
                author_object.fans.append(user_object)
                author_object.fans_count += 1
                db.session.commit()
                return create_response(
                    OBJECT_CREATED_RESPONSE, user_object.as_dict(), language=language
                )
            else:
                return create_response(USER_ALREADY_IN_FANS_RESPONSE, language=language)
        return create_response(USER_NOT_FOUND_RESPONSE, language=language)

    def delete(self) -> Response:
        args: dict = self.post_parser.parse_args()
        language: str = args.get("language")
        user_id: int = args.get("user_id")
        author_id: int = args.get("author_id")
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        user_query = user.User.query
        author_query = author.Author.query
        user_query = user_query.filter_by(id=user_id)
        author_query = author_query.filter_by(id=author_id)

        author_object: author.Author = author_query.first()
        user_object = user_query.first()

        if author_query:
            if user_object in author_query.fans:
                author_query.fans.remove(user_object)
                author_object.fans_count += 1
                db.session.commit()
                return create_response(
                    OBJECT_REMOVED_RESPONSE, author_object.as_dict(), language=language
                )
            else:
                return create_response(USER_NOT_IN_FANS_RESPONSE, language=language)
        return create_response(USER_NOT_FOUND_RESPONSE, language=language)
