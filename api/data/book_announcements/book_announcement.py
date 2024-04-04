import datetime

from flask import Response
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import RequestParser
from models import book_announcement
from models.user import User
from helpers.request_response import create_response
from static.responses import TOKEN_INVALID_RESPONSE, INSUFFICIENT_PERMISSIONS_RESPONSE, \
    OBJECT_MODIFIED_RESPONSE, OBJECT_DELETED_RESPONSE, OBJECT_CREATED_RESPONSE, BOOK_ANNOUNCEMENT_OBJECT_RESPONSE, \
    BOOK_ANNOUNCEMENT_OBJECTS_LIST_RESPONSE, OBJECT_NOT_FOUND_RESPONSE


class BookAnnouncement(Resource):
    def __init__(self) -> None:
        self.get_parser: RequestParser = RequestParser()
        self.get_parser.add_arg("id", type=int, required=False)
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("title")
        self.post_parser.add_arg("author")
        self.post_parser.add_arg("publishing_house")
        self.post_parser.add_arg("description")
        self.post_parser.add_arg("genres", type=list)
        self.post_parser.add_arg("picture")
        self.post_parser.add_arg("premiere_date")
        self.delete_parser: RequestParser = RequestParser()
        self.delete_parser.add_arg("id", type=int)
        self.patch_parser: RequestParser = RequestParser()
        self.patch_parser.add_arg("id", type=int)
        self.patch_parser.add_arg("title")
        self.patch_parser.add_arg("author")
        self.patch_parser.add_arg("publishing_house")
        self.patch_parser.add_arg("description")
        self.patch_parser.add_arg("genres", type=list)
        self.patch_parser.add_arg("picture")
        self.patch_parser.add_arg("premiere_date")
        super(BookAnnouncement, self).__init__()

    def get(self) -> Response:
        args: dict = self.get_parser.parse_args()
        book_announcement_id: int = args.get("id")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE)
        if book_announcement_id:
            book_announcement_object: book_announcement.BookAnnouncement = (
                book_announcement.BookAnnouncement.query.filter_by(
                    id=book_announcement_id
                ).first()
            )
            if not book_announcement_object:
                return create_response(OBJECT_NOT_FOUND_RESPONSE)
            return create_response(BOOK_ANNOUNCEMENT_OBJECT_RESPONSE, book_announcement_object.as_dict())
        book_announcement_objects: list[
            book_announcement.BookAnnouncement
        ] = book_announcement.BookAnnouncement.query.all()
        return create_response(
            BOOK_ANNOUNCEMENT_OBJECTS_LIST_RESPONSE,
            {"book_announcements": [book_object.as_dict() for book_object in book_announcement_objects]})

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        title: str = args.get("title")
        author: int = args.get("author")
        publishing_house: str = args.get("publishing_house")
        description: str = args.get("description")
        genres: list[int] = args.get("genres")
        picture: str = args.get("picture")
        premiere_date: datetime.datetime = args.get("premiere_date")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE)

        # TODO A CO JEŚLI AUTOR O TAKIM ID NIE ISTNIEJE?
        book_announcement_object: book_announcement.BookAnnouncement = (
            book_announcement.BookAnnouncement(
                title=title,
                author=author,
                publishing_house=publishing_house,
                description=description,
                genres=genres,
                picture=picture,
                premiere_date=premiere_date,
            )
        )
        db.session.add(book_announcement_object)
        db.session.commit()

        return create_response(OBJECT_CREATED_RESPONSE)

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        book_announcement_id: int = args.get("id")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE)

        opinion_object: book_announcement.BookAnnouncement = (
            book_announcement.BookAnnouncement.query.filter_by(
                id=book_announcement_id
            ).first()
        )

        db.session.delete(opinion_object)
        db.session.commit()

        return create_response(OBJECT_DELETED_RESPONSE)

    def patch(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        book_announcement_id: int = args.get("id")
        title: str = args.get("title")
        publishing_house: str = args.get("publishing_house")
        description: str = args.get("description")
        genres: list[int] = args.get("genres")
        picture: str = args.get("picture")
        premiere_date: datetime.datetime = args.get("premiere_date")
        email: str | None = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE)
        user: User = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return create_response(INSUFFICIENT_PERMISSIONS_RESPONSE)

        modified_book: book_announcement.BookAnnouncement = (
            book_announcement.BookAnnouncement.query.filter_by(
                id=book_announcement_id
            ).first()
        )

        if user:
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

        return create_response(OBJECT_MODIFIED_RESPONSE)
