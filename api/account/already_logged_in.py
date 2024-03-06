from __future__ import annotations

from flask import Response, jsonify, make_response, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_restful import Resource
from loguru import logger

from helpers.blocklist import BLOCKED_USER_TOKENS, LOGGED_IN_USER_TOKENS


class CheckIfLoggedIn(Resource):
    def __init__(self) -> None:
        super(CheckIfLoggedIn, self).__init__()

    def get(self) -> Response:
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            auth: str | None = request.headers.get("Authorization")
            token: str = ""
            if auth:
                token = auth.split(" ")[1]
            logger.info("TOKEN: " + token)
            logger.info("LOGGED_IN_USER_TOKENS: " + str(LOGGED_IN_USER_TOKENS))
            logger.info("BLOCKED_USER_TOKENS: " + str(BLOCKED_USER_TOKENS))
            if (
                token in BLOCKED_USER_TOKENS
                and current_user not in LOGGED_IN_USER_TOKENS.keys()
            ):
                return make_response(
                    jsonify(msg="Token has expired"),
                    401,
                )
            return make_response(
                jsonify(msg="Token valid"),
                200,
            )
        except AttributeError as e:
            logger.error(e)
            return make_response(jsonify(msg="Token has expired"), 401)
