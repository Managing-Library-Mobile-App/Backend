from flask import Response, jsonify, make_response
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_parser import RequestParser
from models import opinion
from models.user import User


class Opinion(Resource):
    def __init__(self) -> None:
        self.get_parser: RequestParser = RequestParser()
        self.get_parser.add_arg("id", type=int, required=False)
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("account_id", type=int)
        self.post_parser.add_arg("book_id", type=int)
        self.post_parser.add_arg("stars_count", type=int)
        self.post_parser.add_arg("comment")
        self.delete_parser: RequestParser = RequestParser()
        self.delete_parser.add_arg("id", type=int)
        self.patch_parser: RequestParser = RequestParser()
        self.patch_parser.add_arg("id", type=int)
        self.patch_parser.add_arg("stars_count", type=int, required=False)
        self.patch_parser.add_arg("comment", type=str, required=False)
        super(Opinion, self).__init__()

    def get(self) -> Response:
        args: dict = self.get_parser.parse_args()
        opinion_id: int = args.get("id")
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
                    details="Insufficient permissions. Requires admin or being opinion's owner",
                ),
                404,
            )

        if opinion_id:
            opinion_object: opinion.Opinion = opinion.Opinion.query.filter_by(
                id=opinion_id
            ).first()
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
        opinion_objects: list[opinion.Opinion] = opinion.Opinion.query.all()
        return make_response(
            jsonify(*[opinion_object.as_dict() for opinion_object in opinion_objects]),
            200,
        )

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        account_id: int = args.get("account_id")
        book_id: int = args.get("book_id")
        stars_count: int = args.get("stars_count")
        comment: str = args.get("comment")
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

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        opinion_id: int = args.get("id")
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

        opinion_object: opinion.Opinion = opinion.Opinion.query.filter_by(
            id=opinion_id
        ).first()

        db.session.delete(opinion_object)
        db.session.commit()

        return make_response(
            jsonify(message="opinion_deleted", details="Opinion deleted."),
            200,
        )

    def patch(self) -> Response:
        args: dict = self.patch_parser.parse_args()
        opinion_id: int = args.get("id")
        stars_count: int = args.get("stars_count")
        comment: str = args.get("comment")
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
