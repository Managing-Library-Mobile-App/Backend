from flask_restful import Resource, reqparse


class ChangePassword(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            location="json",
        )
        super(ChangePassword, self).__init__()

    def patch(self) -> dict[str, bool | str]:
        args = self.reqparse.parse_args()
        username = args.get("username")
        # TODO weryfikacja w bazie czy taki użytkownik wgl istnieje
        # TODO weryfikacja sesji czy faktycznie ktoś z danym username ma aktywną sesję i jest to ta, która jest
        # w zapytaniu
        # TODO odkomentować
        # if False:
        #     return {
        #         "deleted": True,
        #         "message": "user_not_logged_in",
        #         "details": "User not logged in (No session)",
        #     }
        if username == "Admin-1234":
            return {
                "password_changed": True,
                "message": "password_changed",
                "details": "User deleted successfully",
            }
        return {
            "password_changed": False,
            "message": "user_does_not_exist",
            "details": "User does not exist",
        }
