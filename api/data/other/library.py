from __future__ import annotations

from flask import jsonify, Response, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restful import Resource, reqparse

from models import library
from helpers.init import db

from models.user import User


class Library(Resource):
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
            "read_books",
            type=list,
            required=False,
            location="json",
        )
        self.post_parser.add_argument(
            "bought_books",
            type=list,
            required=False,
            location="json",
        )
        self.post_parser.add_argument(
            "favourite_books",
            type=list,
            required=False,
            location="json",
        )
        self.post_parser.add_argument(
            "user_id",
            type=int,
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
            "read_books",
            type=list,
            required=False,
            location="json",
        )
        self.patch_parser.add_argument(
            "bought_books",
            type=list,
            required=False,
            location="json",
        )
        self.patch_parser.add_argument(
            "favourite_books",
            type=list,
            required=False,
            location="json",
        )
        super(Library, self).__init__()

    @jwt_required()
    def get(self) -> Response:
        args = self.get_parser.parse_args()
        library_id = args.get("id")
        try:
            verify_jwt_in_request()
            email = get_jwt_identity()
        except AttributeError:
            return make_response(
                jsonify(
                    password_changed=False,
                    message="user_not_logged_in",
                    details="User not logged in (No session)",
                ),
                401,
            )
        library_object: library.Library = library.Library.query.filter_by(
            id=library_id
        ).first()
        user = User.query.filter_by(email=email).first()
        if not user.is_admin:
            if not user.id == library_object.user_id:
                return make_response(
                    jsonify(
                        message="insufficient_permissions",
                        details="Insufficient permissions. Requires admin or being library's owner",
                    ),
                    404,
                )

        return make_response(
            jsonify(library_object.as_dict()),
            200,
        )

    @jwt_required()
    def post(self) -> Response:
        args = self.post_parser.parse_args()
        read_books = args.get("read_books")
        bought_books = args.get("bought_books")
        favourite_books = args.get("favourite_books")
        user_id = args.get("user_id")
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

        # TODO A CO JEŚLI USER O TAKIM ID NIE ISTNIEJE?
        library_object: library.Library = library.Library(
            read_books=read_books,
            bought_books=bought_books,
            favourite_books=favourite_books,
            user_id=user_id,
        )
        db.session.add(library_object)
        db.session.commit()

        return make_response(
            jsonify(message="library_created", details="Library created."),
            200,
        )

    @jwt_required()
    def delete(self) -> Response:
        args = self.delete_parser.parse_args()
        library_id = args.get("id")
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

        library_object: library.Library = library.Library.query.filter_by(
            id=library_id
        ).first()

        db.session.delete(library_object)
        db.session.commit()

        return make_response(
            jsonify(message="library_deleted", details="Library deleted."),
            200,
        )

    @jwt_required()
    def patch(self) -> Response:
        args = self.delete_parser.parse_args()
        library_id = args.get("id")
        read_books = args.get("read_books")
        bought_books = args.get("bought_books")
        favourite_books = args.get("favourite_books")
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

        modified_library = library.Library.query.filter_by(id=library_id).first()

        if user:
            if read_books:
                modified_library.read_books = read_books
            if bought_books:
                modified_library.bought_books = bought_books
            if favourite_books:
                modified_library.favourite_books = favourite_books
            db.session.commit()

        return make_response(
            jsonify(message="library_modified", details="Library modified."),
            200,
        )
