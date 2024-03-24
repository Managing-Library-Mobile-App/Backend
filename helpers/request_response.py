from typing import Any

from flask import make_response, jsonify, Response
from flask_restful import reqparse


class RequestParser(reqparse.RequestParser):
    """Custom request parser class."""

    def add_arg(
            self, name: str, type: type = str, required: bool = True, **kwargs
    ) -> None:
        """
        Modified version of add_argument
        :returns: None
        :rtype: None
        """
        self.add_argument(name, type=type, required=required, location="json", **kwargs)


def create_response(static_response: (dict[str, Any], int),
                    dynamic_response_data: dict[str, Any] = None) -> Response:
    response_body = static_response[0]
    if dynamic_response_data:
        for key, value in dynamic_response_data.items():
            response_body[key] = value
    status_code = static_response[1]
    return make_response(
        jsonify(response_body), status_code
    )
