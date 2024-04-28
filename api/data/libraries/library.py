from flask import Response, request
from flask_restful import Resource

from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import create_response
from models import library
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    LIBRARIES_RESPONSE,
)


class Library(Resource):
    def __init__(self) -> None:
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
        library_objects = library_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
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
