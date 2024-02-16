from flask_restful import Resource, reqparse


class Logout(Resource):
    """Test Description"""

    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        super(Logout, self).__init__()

    def post(self) -> dict[str, bool | str]:
        pass
