import json

from flask import make_response, jsonify, Response, abort
from flask_restful import reqparse
from flask_restful.reqparse import Argument

from helpers.translation import (
    translate_dict_to_known,
    translate_list_to_known,
)
from static.responses import LENGTH_VALIDATION_ERROR_RESPONSE


def int_range_validation(min=0, max=255):
    def validate(value):
        if not isinstance(value, int):
            raise ValueError("Invalid literal for integer(): {0}".format(value))
        if min <= value <= max:
            return value
        raise ValueError(f"Value must be an integer in range [{min}, {max}]")

    return validate


def string_range_validation(min=0, max=255):
    def validate(value):
        if not isinstance(value, str):
            raise ValueError("Invalid literal for str(): {0}".format(value))
        if min <= len(value) <= max:
            return value
        raise ValueError(f"Value must be a str with length in range [{min}, {max}]")

    return validate


class APIArgument(Argument):
    def __init__(self, *args, **kwargs):
        super(APIArgument, self).__init__(*args, **kwargs)

    def handle_validation_error(self, error, bundle_errors):
        help_str = "(%s) " % self.help if self.help else ""
        details = "[%s]: %s%s" % (self.name, help_str, str(error))
        return abort(
            Response(
                json.dumps(LENGTH_VALIDATION_ERROR_RESPONSE[0]),
                mimetype="application/json",
                status=LENGTH_VALIDATION_ERROR_RESPONSE[1],
            )
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
