from __future__ import annotations

from flask import jsonify, Response, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restful import Resource, reqparse

from models import book_announcement
from helpers.init import db

from models.user import User


class BookAnnouncement(Resource):
    def __init__(self) -> None:
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument(
            "id",
            type=int,
            required=True,
            location="json",
        )
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            "title",
            type=str,
            required=True,
            location="json",
        )
        self.post_parser.add_argument(
            "author",
            type=str,
            required=True,
            location="json",
        )
        self.post_parser.add_argument(
            "publishing_house",
            type=str,
            required=True,
            location="json",
        )
        self.post_parser.add_argument(
            "description",
            type=str,
            required=True,
            location="json",
        )
        self.post_parser.add_argument(
            "genres",
            type=list,
            required=True,
            location="json",
        )
        self.post_parser.add_argument(
            "picture",
            type=str,
            required=True,
            location="json",
        )
        self.post_parser.add_argument(
            "premiere_date",
            type=str,
            required=True,
            location="json",
        )
        self.delete_parser = reqparse.RequestParser()
        self.delete_parser.add_argument(
            "id",
            type=int,
            required=True,
            location="json",
        )
        self.patch_parser = reqparse.RequestParser()
        self.patch_parser.add_argument(
            "id",
            type=int,
            required=True,
            location="json",
        )
        self.patch_parser.add_argument(
            "title",
            type=str,
            required=True,
            location="json",
        )
        self.patch_parser.add_argument(
            "author",
            type=str,
            required=True,
            location="json",
        )
        self.patch_parser.add_argument(
            "publishing_house",
            type=str,
            required=True,
            location="json",
        )
        self.patch_parser.add_argument(
            "description",
            type=str,
            required=True,
            location="json",
        )
        self.patch_parser.add_argument(
            "genres",
            type=list,
            required=True,
            location="json",
        )
        self.patch_parser.add_argument(
            "picture",
            type=str,
            required=True,
            location="json",
        )
        self.patch_parser.add_argument(
            "premiere_date",
            type=str,
            required=True,
            location="json",
        )
        super(BookAnnouncement, self).__init__()

    @jwt_required()
    def get(self) -> Response:
        args = self.get_parser.parse_args()
        book_announcement_id = args.get("id")
        try:
            verify_jwt_in_request()
            get_jwt_identity()
        except AttributeError:
            return make_response(
                jsonify(
                    password_changed=False,
                    message="user_not_logged_in",
                    details="User not logged in (No session)",
                ),
                401,
            )
        book_announcement_object: book_announcement.BookAnnouncement = (
            book_announcement.BookAnnouncement.query.filter_by(
                id=book_announcement_id
            ).first()
        )
        return make_response(
            jsonify(book_announcement_object.as_dict()),
            200,
        )

    @jwt_required()
    def post(self) -> Response:
        args = self.post_parser.parse_args()
        title = args.get("title")
        author = args.get("author")
        publishing_house = args.get("publishing_house")
        description = args.get("description")
        genres = args.get("genres")
        picture = args.get("picture")
        premiere_date = args.get("premiere_date")
        try:
            verify_jwt_in_request()
            email = get_jwt_identity()
        except AttributeError:
            return make_response(
                jsonify(
                    message="user_not_logged_in",
                    details="User not logged in (No session)",
                ),
                401,
            )
        user = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return make_response(
                jsonify(
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin status.",
                ),
                404,
            )

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

        return make_response(
            jsonify(
                message="book_announcement_created",
                details="Book Announcement created.",
            ),
            200,
        )

    @jwt_required()
    def delete(self) -> Response:
        args = self.delete_parser.parse_args()
        book_announcement_id = args.get("id")
        try:
            verify_jwt_in_request()
            email = get_jwt_identity()
        except AttributeError:
            return make_response(
                jsonify(
                    message="user_not_logged_in",
                    details="User not logged in (No session)",
                ),
                401,
            )
        user = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return make_response(
                jsonify(
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin status.",
                ),
                404,
            )

        opinion_object: book_announcement.BookAnnouncement = (
            book_announcement.BookAnnouncement.query.filter_by(
                id=book_announcement_id
            ).first()
        )

        db.session.delete(opinion_object)
        db.session.commit()

        return make_response(
            jsonify(
                message="book_announcement_deleted",
                details="Book announcement deleted.",
            ),
            200,
        )

    @jwt_required()
    def patch(self) -> Response:
        args = self.delete_parser.parse_args()
        book_announcement_id = args.get("id")
        title = args.get("title")
        publishing_house = args.get("publishing_house")
        description = args.get("description")
        genres = args.get("genres")
        picture = args.get("picture")
        premiere_date = args.get("premiere_date")
        try:
            verify_jwt_in_request()
            email = get_jwt_identity()
        except AttributeError:
            return make_response(
                jsonify(
                    message="user_not_logged_in",
                    details="User not logged in (No session)",
                ),
                401,
            )
        user = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return make_response(
                jsonify(
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin status.",
                ),
                404,
            )

        modified_book = book_announcement.BookAnnouncement.query.filter_by(
            id=book_announcement_id
        ).first()

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

        return make_response(
            jsonify(
                message="book_announcement_modified",
                details="Book announcement modified.",
            ),
            200,
        )
