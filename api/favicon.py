from flask import Response, current_app
from flask_restful import Resource


class Favicon(Resource):
    def get(self) -> Response:
        return current_app.send_static_file("favicon.ico")
