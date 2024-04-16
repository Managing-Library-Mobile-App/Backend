from flask import make_response, jsonify, Response
from flask_restful import reqparse

from helpers.translation import (
    translate_dict_to_known,
    translate_list_to_known,
)


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


def create_response(
    static_response: (dict | list, int),
    dynamic_response_data: dict | list = None,
    language: str = None,
    not_translated: set[str] = None,
) -> Response:
    if not_translated is None:
        not_translated = {"message"}
    else:
        not_translated.add("message")

    response_body: dict | list = static_response[0]
    if isinstance(dynamic_response_data, dict):
        for key, value in dynamic_response_data.items():
            response_body[key] = value
    elif isinstance(dynamic_response_data, list):
        response_body = dynamic_response_data
    if language:
        if isinstance(response_body, dict):
            response_body = translate_dict_to_known(
                response_body, language, not_translated
            )
        else:
            response_body = translate_list_to_known(
                response_body, language, not_translated
            )
    status_code = static_response[1]
    return make_response(jsonify(response_body), status_code)
