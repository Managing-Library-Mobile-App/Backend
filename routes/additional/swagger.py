import json

from flask import jsonify
from flask_restful import Resource
from flask_swagger_ui import get_swaggerui_blueprint

# Dodanie dokumentacji Swagger
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Library API"}
)


class Swagger(Resource):
    def get(self):
        with open("swagger/swagger.json", "r") as f:
            return jsonify(json.load(f))
