from flask_restful import Resource, reqparse


class DeleteAccount(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            location="json",
        )
        super(DeleteAccount, self).__init__()

    def delete(self) -> dict[str, bool | str]:
        args = self.reqparse.parse_args()
        username = args.get("username")
        # TODO weryfikacja sesji czy faktycznie ktoś z danym username ma aktywną sesję i jest to ta, która jest
        # w zapytaniu
        # TODO odkomentować
        # if False:
        #     return {
        #         "deleted": True,
        #         "message": "user_not_logged_in",
        #         "details": "User not logged in (No session)",
        #     }
        # TODO weryfikacja w bazie czy taki użytkownik wgl istnieje
        if username == "Admin1234":
            # TODO wyrzucenie sesji po usunięciu użytkownika
            return {
                "deleted": True,
                "message": "user_deleted",
                "details": "User deleted successfully",
            }
        return {
            "deleted": False,
            "message": "user_does_not_exist",
            "details": "User does not exist",
        }
