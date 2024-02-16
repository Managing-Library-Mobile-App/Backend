from flask_restful import Resource, reqparse
from flask_restful_swagger import swagger


class Logout(Resource):
    """Test Description"""

    @swagger.operation(notes="test_note")
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        super(Logout, self).__init__()

    def post(self) -> dict[str, bool | str]:
        pass
