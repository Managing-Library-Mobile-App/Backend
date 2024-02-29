from __future__ import annotations

from flask import jsonify, Response, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restful import Resource

from helpers.jwt_auth import verify_jwt_token
from helpers.request_parser import RequestParser
from models import author
from helpers.init import db

from models.user import User


class Author(Resource):
    def __init__(self) -> None:
        self.get_parser = RequestParser()
        self.get_parser.add_arg("id", type=int, required=False)

        self.post_parser = RequestParser()
        self.post_parser.add_arg("name")
        self.post_parser.add_arg("genres", type=list)
        self.post_parser.add_arg("biography")
        self.post_parser.add_arg("picture")
        self.post_parser.add_arg("fans", type=list, required=False)
        self.post_parser.add_arg("released_books", type=list, required=False)

        self.delete_parser = RequestParser()
        self.delete_parser.add_arg("id", type=int)

        self.patch_parser = RequestParser()
        self.patch_parser.add_arg("id", type=int)
        self.patch_parser.add_arg("name", required=False)
        self.patch_parser.add_arg("genres", type=list, required=False)
        self.patch_parser.add_arg("biography", required=False)
        self.patch_parser.add_arg("picture", required=False)

        super(Author, self).__init__()

    @jwt_required()
    def get(self) -> Response:
        args = self.get_parser.parse_args()
        author_id = args.get("id")
        verification_output = verify_jwt_token()
        if type(verification_output) is str:
            email = verification_output
        else:
            return make_response(verification_output, 401)
        if author_id:
            author_object: author.Author = author.Author.query.filter_by(
                id=author_id
            ).first()
            return make_response(
                jsonify(author_object.as_dict()),
                200,
            )
        author_objects: list[author.Author] = author.Author.query.all()
        return make_response(
            jsonify(*[author_object.as_dict() for author_object in author_objects]),
            200,
        )

    @jwt_required()
    def post(self) -> Response:
        args = self.post_parser.parse_args()
        name = args.get("name")
        genres = args.get("genres")
        biography = args.get("biography")
        picture = args.get("picture")
        fans = args.get("fans")
        released_books = args.get("released_books")
        verification_output = verify_jwt_token()
        if type(verification_output) is str:
            email = verification_output
        else:
            return make_response(verification_output, 401)
        user = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return make_response(
                jsonify(
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin status.",
                ),
                404,
            )

        # TODO A CO JEŚLI FANS LUB RELEASED_BOOKS O TAKICH ID NIE ISTNIEJE?
        author_object: author.Author = author.Author(
            name=name,
            genres=genres,
            biography=biography,
            picture=picture,
            fans=fans if fans else [],
            released_books=released_books if released_books else [],
        )
        db.session.add(author_object)
        db.session.commit()

        return make_response(
            jsonify(message="author_created", details="Author created."),
            200,
        )

    @jwt_required()
    def delete(self) -> Response:
        args = self.delete_parser.parse_args()
        author_id = args.get("id")
        verification_output = verify_jwt_token()
        if type(verification_output) is str:
            email = verification_output
        else:
            return make_response(verification_output, 401)
        user = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return make_response(
                jsonify(
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin status.",
                ),
                404,
            )

        author_object: author.Author = author.Author.query.filter_by(
            id=author_id
        ).first()

        db.session.delete(author_object)
        db.session.commit()

        return make_response(
            jsonify(message="author_deleted", details="Author deleted."),
            200,
        )

    @jwt_required()
    def patch(self) -> Response:
        args = self.delete_parser.parse_args()
        author_id = args.get("id")
        name = args.get("name")
        genres = args.get("genres")
        biography = args.get("biography")
        picture = args.get("picture")
        verification_output = verify_jwt_token()
        if type(verification_output) is str:
            email = verification_output
        else:
            return make_response(verification_output, 401)
        user = User.query.filter_by(email=email).first()
        if not user.is_admin:
            return make_response(
                jsonify(
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin status.",
                ),
                404,
            )

        modified_author = author.Author.query.filter_by(id=author_id).first()

        if user:
            if name:
                modified_author.name = name
            if genres:
                modified_author.genres = genres
            if biography:
                modified_author.biography = biography
            if picture:
                modified_author.picture = picture
            db.session.commit()

        return make_response(
            jsonify(message="author_modified", details="Author modified."),
            200,
        )
