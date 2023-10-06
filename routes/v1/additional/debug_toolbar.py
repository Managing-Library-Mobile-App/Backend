from flask_restful import Resource


class DebugToolbar(Resource):
    def get(self):
        return "<html><body></body></html>"
