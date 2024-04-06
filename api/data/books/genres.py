from flask import Response
from flask_restful import Resource

from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import create_response, RequestParser
from static.responses import TOKEN_INVALID_RESPONSE, GENRES_LIST_RESPONSE


class Book(Resource):
    def __init__(self) -> None:
        self.get_parser: RequestParser = RequestParser()
        self.get_parser.add_arg("language", required=False)
        super(Book, self).__init__()

    def get(self) -> Response:
        args: dict = self.get_parser.parse_args()
        language: str = args.get("language")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        available_genres_list: list[str] = [
            "Fantasy, Science fiction",
            "Thriller, Horror, Mystery and detective stories",
            "Young Adult",
            "Romance",
            "History",
            "Action & Adventure",
            "Biography",
            "Popular Science",
            "Children's",
            "Poetry, Plays",
            "Comic books",
        ]

        return create_response(
            GENRES_LIST_RESPONSE, {"genres": available_genres_list}, language=language
        )
