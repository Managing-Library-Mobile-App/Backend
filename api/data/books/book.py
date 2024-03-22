import datetime

from flask import Response, jsonify, make_response
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_parser import RequestParser
from models import book
from models.user import User


class Book(Resource):
    def __init__(self) -> None:
        self.get_parser: RequestParser = RequestParser()
        self.get_parser.add_arg("id", type=int, required=False)
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("isbn", type=int)
        self.post_parser.add_arg("title")
        self.post_parser.add_arg("author_id")
        self.post_parser.add_arg("publishing_house")
        self.post_parser.add_arg("description")
        self.post_parser.add_arg("genres", type=list)
        self.post_parser.add_arg("picture")
        self.post_parser.add_arg("premiere_date")
        self.delete_parser: RequestParser = RequestParser()
        self.delete_parser.add_arg("id", type=int)
        self.patch_parser: RequestParser = RequestParser()
        self.patch_parser.add_arg("id", type=int)
        self.patch_parser.add_arg("isbn")
        self.patch_parser.add_arg("title")
        self.patch_parser.add_arg("author_id")
        self.patch_parser.add_arg("publishing_house")
        self.patch_parser.add_arg("description")
        self.patch_parser.add_arg("genres", type=list)
        self.patch_parser.add_arg("picture")
        self.patch_parser.add_arg("premiere_date")
        super(Book, self).__init__()

    def get(self) -> Response:
        args: dict = self.get_parser.parse_args()
        book_id: int = args.get("id")
        verification_output: Response | str = verify_jwt_token()
        if type(verification_output) is str:
            pass
        else:
            return make_response(verification_output, 401)

        if book_id:
            book_object: book.Book = book.Book.query.filter_by(id=book_id).first()
            return make_response(
                jsonify(book_object.as_dict()),
                200,
            )
        book_objects: list[book.Book] = book.Book.query.all()
        return make_response(
            jsonify(*[book_object.as_dict() for book_object in book_objects]),
            200,
        )

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        isbn: str = args.get("isbn")
        title: str = args.get("title")
        author_id: int = args.get("author_id")
        publishing_house: str = args.get("publishing_house")
        description: str = args.get("description")
        genres: list[int] = args.get("genres")
        picture: str = args.get("picture")
        premiere_date: datetime.datetime = args.get("premiere_date")
        verification_output: Response | str = verify_jwt_token()
        if type(verification_output) is str:
            email: str = verification_output
        else:
            return make_response(verification_output, 401)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return make_response(
                jsonify(
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin status.",
                ),
                404,
            )

        # TODO A CO JEŚLI AUTOR O TAKIM ID NIE ISTNIEJE?
        book_object: book.Book = book.Book(
            isbn=isbn,
            title=title,
            author_id=author_id,
            publishing_house=publishing_house,
            description=description,
            genres=genres,
            picture=picture,
            premiere_date=premiere_date,
        )
        db.session.add(book_object)
        db.session.commit()

        return make_response(
            jsonify(message="book_created", details="Book created."),
            200,
        )

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        book_id: int = args.get("id")
        verification_output: Response | str = verify_jwt_token()
        if type(verification_output) is str:
            email: str = verification_output
        else:
            return make_response(verification_output, 401)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return make_response(
                jsonify(
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin status.",
                ),
                404,
            )

        opinion_object: book.Book = book.Book.query.filter_by(id=book_id).first()

        db.session.delete(opinion_object)
        db.session.commit()

        return make_response(
            jsonify(message="book_deleted", details="Book deleted."),
            200,
        )

    def patch(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        book_id: int = args.get("id")
        isbn: str = args.get("isbn")
        title: str = args.get("title")
        publishing_house: str = args.get("publishing_house")
        description: str = args.get("description")
        genres: list[int] = args.get("genres")
        picture: str = args.get("picture")
        premiere_date: datetime.datetime = args.get("premiere_date")
        verification_output: Response | str = verify_jwt_token()
        if type(verification_output) is str:
            email: str = verification_output
        else:
            return make_response(verification_output, 401)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return make_response(
                jsonify(
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin status.",
                ),
                404,
            )

        modified_book: book.Book = book.Book.query.filter_by(id=book_id).first()

        if user:
            if isbn:
                modified_book.isbn = isbn
            if title:
                modified_book.title = title
            if publishing_house:
                modified_book.publishing_house = publishing_house
            if description:
                modified_book.description = description
            if genres:
                modified_book.genres = genres
            if picture:
                modified_book.picture = picture
            if premiere_date:
                modified_book.premiere_date = premiere_date
            db.session.commit()

        return make_response(
            jsonify(message="book_modified", details="Book modified."),
            200,
        )
