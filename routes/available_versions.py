from flask import json
from flask_restful import Resource


class AvailableVersions(Resource):
    def get(self):
        return json.jsonify({"versions": "v1"})
