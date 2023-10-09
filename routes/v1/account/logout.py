from flask_restful import Resource, reqparse


class Logout(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            location="json",
        )
        super(Logout, self).__init__()

    def post(self) -> dict[str, bool | str]:
        args = self.reqparse.parse_args()
        username = args.get("username")
        # TODO weryfikacja sesji czy faktycznie ktoś z danym username ma aktywną sesję i jest to ta, która jest
        # w zapytaniu
        # TODO odkomentować
        # if False:
        #     return {
        #         "logged_out": False,
        #         "message": "user_not_logged_in",
        #         "details": "User not logged in (No session)",
        #     }
        # TODO weryfikacja w bazie czy taki użytkownik wgl istnieje
        if username == "Admin-1234":
            # TODO wyrzucenie sesji po usunięciu użytkownika
            return {
                "logged_out": True,
                "message": "user_deleted",
                "details": "User deleted successfully",
            }
        return {
            "logged_out": False,
            "message": "user_does_not_exist",
            "details": "User does not exist",
        }
