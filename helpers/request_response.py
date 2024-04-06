from typing import Any

from flask import make_response, jsonify, Response
from flask_restful import reqparse

from helpers.translation import (
    translate_any_to_known,
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
    static_response: (dict[str, Any], int),
    dynamic_response_data: dict[str, Any] = None,
    language: str = None,
    not_translated: set[str] = None,
) -> Response:
    response_body = static_response[0]
    if dynamic_response_data:
        for key, value in dynamic_response_data.items():
            response_body[key] = value
    if language:
        if not_translated is None:
            not_translated = {"message"}
        else:
            not_translated.add("message")
        for key, value in response_body.items():
            if key not in not_translated:
                if isinstance(value, dict):
                    response_body[key] = translate_dict_to_known(
                        value, language, not_translated
                    )
                elif (
                    isinstance(value, list)
                    or isinstance(value, tuple)
                    or isinstance(value, set)
                ):
                    response_body[key] = translate_list_to_known(
                        response_body[key], language, not_translated
                    )
                elif isinstance(value, str):
                    response_body[key] = translate_any_to_known(
                        response_body[key], language
                    )
    status_code = static_response[1]
    return make_response(jsonify(response_body), status_code)
