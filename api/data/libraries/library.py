from flask import Response, jsonify, make_response
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_parser import RequestParser
from models import library
from models.user import User


class Library(Resource):
    def __init__(self) -> None:
        self.get_parser: RequestParser = RequestParser()
        self.get_parser.add_arg("id", type=int, required=False)
        self.post_parser: RequestParser = RequestParser()
        self.post_parser.add_arg("read_books", type=list, required=False)
        self.post_parser.add_arg("bought_books", type=list, required=False)
        self.post_parser.add_arg("favourite_books", type=list, required=False)
        self.post_parser.add_arg("user_id", type=int)
        self.delete_parser: RequestParser = RequestParser()
        self.delete_parser.add_arg("id", type=int)
        self.patch_parser: RequestParser = RequestParser()
        self.patch_parser.add_arg("id", type=int)
        self.patch_parser.add_arg("read_books", type=list, required=False)
        self.patch_parser.add_arg("bought_books", type=list, required=False)
        self.patch_parser.add_arg("favourite_books", type=list, required=False)
        super(Library, self).__init__()

    def get(self) -> Response:
        args: dict = self.get_parser.parse_args()
        library_id: int = args.get("id")
        verification_output: Response | str = verify_jwt_token()
        if type(verification_output) is str:
            email: str = verification_output
        else:
            return make_response(verification_output, 401)
        user: User = User.query.filter_by(email=email).first()
        if library_id:
            library_object: library.Library = library.Library.query.filter_by(
                id=library_id
            ).first()
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
        if not user.is_admin:
            return make_response(
                jsonify(
                    message="insufficient_permissions",
                    details="Insufficient permissions. Requires admin or being library's owner",
                ),
                404,
            )
        library_objects: list[library.Library] = library.Library.query.all()
        return make_response(
            jsonify(*[library_object.as_dict() for library_object in library_objects]),
            200,
        )

    def post(self) -> Response:
        args: dict = self.post_parser.parse_args()
        read_books: list[int] = args.get("read_books")
        bought_books: list[int] = args.get("bought_books")
        favourite_books: list[int] = args.get("favourite_books")
        user_id: int = args.get("user_id")
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

        # TODO A CO JEŚLI USER O TAKIM ID NIE ISTNIEJE?
        library_object: library.Library = library.Library(
            read_books=read_books if read_books else [],
            bought_books=bought_books if bought_books else [],
            favourite_books=favourite_books if favourite_books else [],
            user_id=user_id,
        )
        db.session.add(library_object)
        db.session.commit()

        return make_response(
            jsonify(message="library_created", details="Library created."),
            200,
        )

    def delete(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        library_id: int = args.get("id")
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

        library_object: library.Library = library.Library.query.filter_by(
            id=library_id
        ).first()

        db.session.delete(library_object)
        db.session.commit()

        return make_response(
            jsonify(message="library_deleted", details="Library deleted."),
            200,
        )

    def patch(self) -> Response:
        args: dict = self.delete_parser.parse_args()
        library_id: int = args.get("id")
        read_books: list[int] = args.get("read_books")
        bought_books: list[int] = args.get("bought_books")
        favourite_books: list[int] = args.get("favourite_books")
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

        modified_library: library.Library = library.Library.query.filter_by(
            id=library_id
        ).first()

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
