from flask import Response, jsonify, make_response, request
from flask_restful import Resource
from loguru import logger

from helpers.blocklist import BLOCKED_USER_TOKENS, LOGGED_IN_USER_TOKENS
from helpers.jwt_auth import verify_jwt_token


class CheckIfLoggedIn(Resource):
    def __init__(self) -> None:
        super(CheckIfLoggedIn, self).__init__()

    def get(self) -> Response:
        verification_output: Response | str = verify_jwt_token()
        if not type(verification_output) is str:
            return make_response(verification_output, 401)
        auth: str | None = request.headers.get("Authorization")
        token: str = ""
        if auth:
            token = auth.split(" ")[1]
        if token in LOGGED_IN_USER_TOKENS.values():
            return make_response(
                jsonify(msg="Token valid"),
                200,
            )
        return make_response(jsonify(msg="Token invalid"), 401)
