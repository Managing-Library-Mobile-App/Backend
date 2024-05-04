from flask import Response, request
from flask_restful import Resource
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import create_response
from models import book
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    BOOKS_RESPONSE,
)


class SimilarBooks(Resource):
    def __init__(self) -> None:
        super(SimilarBooks, self).__init__()

    def get(self) -> Response:
        language: str = request.args.get("language", type=str)
        id: int = request.args.get("id", type=int)
        if not verify_jwt_token():
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        book_object = book.Book.query.filter(book.Book.id == id).first()

        similar_books_max_count = 10
        similar_book_objects = book.Book.query.all()
        if len(similar_book_objects) >= similar_books_max_count:
            similar_book_objects = similar_book_objects[:similar_books_max_count]

        return create_response(
            BOOKS_RESPONSE,
            {
                "results": [
                    similar_book_object.as_dict()
                    for similar_book_object in similar_book_objects
                ],
                "pagination": {
                    "count": len(similar_book_objects),
                },
            },
            language=language,
            not_translated={"isbn", "title", "publishing_house", "picture"},
        )
