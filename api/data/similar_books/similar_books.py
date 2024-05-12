from flask import Response, request
from flask_restful import Resource
from sqlalchemy import desc

from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import create_response
from models import book, library, user
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    BOOKS_RESPONSE,
)


class SimilarBooks(Resource):
    def __init__(self) -> None:
        super(SimilarBooks, self).__init__()

    def get(self) -> Response:
        language: str = request.args.get("language", type=str)
        email = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        user_object = user.User.query.filter_by(email=email).first()

        library_object: library.Library = library.Library.query.filter_by(
            user_id=user_object.id
        ).first()
        read_books_user = library_object.read_books
        favourite_books_user = library_object.favourite_books
        bought_books_user = library_object.bought_books

        genres_with_count = {}

        for book_object in [
            *read_books_user,
            *favourite_books_user,
            *bought_books_user,
        ]:
            genres = book_object.genres
            for genre in genres:
                if genre not in genres_with_count:
                    genres_with_count[genre] = 1
                else:
                    genres_with_count[genre] += 1

        genre_with_highest_count = None

        for genre, count in genres_with_count.items():
            if not genre_with_highest_count:
                genre_with_highest_count = genre
            elif count > genres_with_count[genre_with_highest_count]:
                genre_with_highest_count = genre

        # teraz pobieramy wszystkie książki dla danego genre_with_highest_count lub jeśli user nie ma żadnych książek
        # ulubionych read i bought to bierzemy najpopularniejszy genre w apce

        if genre_with_highest_count:
            similar_book_objects = book.Book.query.filter(
                book.Book.genres.any(genre_with_highest_count)
            )
        else:
            genres_with_count_all_users = {}
            all_library_objects = library.Library.query.all()
            for library_object in all_library_objects:
                for book_object in [
                    *library_object.read_books,
                    *library_object.bought_books,
                    *library_object.favourite_books,
                ]:
                    genres = book_object.genres
                    for genre in genres:
                        if genre not in genres_with_count_all_users:
                            genres_with_count_all_users[genre] = 1
                        else:
                            genres_with_count_all_users[genre] += 1

            genre_with_highest_count_all_users = None
            for genre, count in genres_with_count_all_users.items():
                if not genre_with_highest_count_all_users:
                    genre_with_highest_count_all_users = genre
                elif (
                    count
                    > genres_with_count_all_users[genre_with_highest_count_all_users]
                ):
                    genre_with_highest_count_all_users = genre
            similar_book_objects = book.Book.query.filter(
                book.Book.genres.any(genre_with_highest_count_all_users)
            )

        similar_books_max_count = 10
        if len(similar_book_objects.all()) >= similar_books_max_count:
            opinions_count_field = getattr(book.Book, "opinions_count")
            premiere_date_field = getattr(book.Book, "premiere_date")

            similar_book_objects = similar_book_objects.filter(book.Book.score > 4)
            similar_book_objects = similar_book_objects.order_by(
                desc(opinions_count_field)
            )
            similar_book_objects = similar_book_objects.order_by(
                desc(premiere_date_field)
            )
            similar_book_objects = similar_book_objects.all()[:similar_books_max_count]

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
