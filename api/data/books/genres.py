from flask import Response, request
from flask_restful import Resource

from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import create_response
from static.responses import TOKEN_INVALID_RESPONSE, GENRES_RESPONSE


class Genres(Resource):
    def __init__(self) -> None:
        super(Genres, self).__init__()

    def get(self) -> Response:
        language: str = request.args.get("language")
        if not verify_jwt_token:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)
        return create_response(GENRES_RESPONSE, language=language)
