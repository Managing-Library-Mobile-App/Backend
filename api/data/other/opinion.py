from __future__ import annotations

from flask import jsonify, Response, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restful import Resource, reqparse

from models import opinion
from helpers.init import db

from models.user import User


class Opinion(Resource):
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
            "account_id",
            type=int,
            required=True,
            location="json",
        )
        self.post_parser.add_argument(
            "book_id",
            type=int,
            required=True,
            location="json",
        )
        self.post_parser.add_argument(
            "stars_count",
            type=int,
            required=True,
            location="json",
        )
        self.post_parser.add_argument(
            "comment",
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
            "stars_count",
            type=int,
            required=False,
            location="json",
        )
        self.patch_parser.add_argument(
            "comment",
            type=str,
            required=False,
            location="json",
        )
        super(Opinion, self).__init__()

    @jwt_required()
    def get(self) -> Response:
        args = self.get_parser.parse_args()
        opinion_id = args.get("id")
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
        opinion_object: opinion.Opinion = opinion.Opinion.query.filter_by(
            id=opinion_id
        ).first()
        user = User.query.filter_by(email=email).first()
        if not user.is_admin:
            if not user.id == opinion_object.user_id:
                return make_response(
                    jsonify(
                        message="insufficient_permissions",
                        details="Insufficient permissions. Requires admin or being library's owner",
                    ),
                    404,
                )

        return make_response(
            jsonify(opinion_object.as_dict()),
            200,
        )

    @jwt_required()
    def post(self) -> Response:
        args = self.post_parser.parse_args()
        account_id = args.get("account_id")
        book_id = args.get("book_id")
        stars_count = args.get("stars_count")
        comment = args.get("comment")
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

        # TODO A CO JEŚLI USER O TAKIM ID LUB KSIĄŻKA NIE ISTNIEJE?
        opinion_object: opinion.Opinion = opinion.Opinion(
            account_id=account_id,
            book_id=book_id,
            stars_count=stars_count,
            comment=comment,
        )
        db.session.add(opinion_object)
        db.session.commit()

        return make_response(
            jsonify(message="opinion_created", details="Opinion created."),
            200,
        )

    @jwt_required()
    def delete(self) -> Response:
        args = self.delete_parser.parse_args()
        opinion_id = args.get("id")
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

        opinion_object: opinion.Opinion = opinion.Opinion.query.filter_by(
            id=opinion_id
        ).first()

        db.session.delete(opinion_object)
        db.session.commit()

        return make_response(
            jsonify(message="opinion_deleted", details="Opinion deleted."),
            200,
        )

    @jwt_required()
    def patch(self) -> Response:
        args = self.delete_parser.parse_args()
        opinion_id = args.get("id")
        stars_count = args.get("stars_count")
        comment = args.get("comment")
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

        modified_opinion = opinion.Opinion.query.filter_by(id=opinion_id).first()

        if user:
            if stars_count:
                modified_opinion.stars_count = stars_count
            if comment:
                modified_opinion.comment = comment
            db.session.commit()

        return make_response(
            jsonify(message="opinion_modified", details="Opinion modified."),
            200,
        )
