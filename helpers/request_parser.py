from flask_restful import reqparse


class RequestParser(reqparse.RequestParser):
    def add_arg(self, name, type="str", required=True, **kwargs):
        self.add_argument(name, type=type, required=required, location="json", **kwargs)
