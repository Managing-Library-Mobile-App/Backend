from __future__ import annotations

from flask import Response, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from loguru import logger

from helpers.blocklist import BLOCKED_USER_TOKENS, LOGGED_IN_USER_TOKENS


class CheckIfLoggedIn(Resource):
    def __init__(self) -> None:
        super(CheckIfLoggedIn, self).__init__()

    def get(self) -> Response:
        try:
            verify_jwt_in_request(optional=True)
            current_user = get_jwt_identity()
            if not current_user:
                raise ValueError()
            auth: str | None = request.headers.get("Authorization")
            token: str = ""
            if auth:
                token = auth.split(" ")[1]
            logger.info("TOKEN: " + token)
            logger.info("LOGGED_IN_USER_TOKENS: " + str(LOGGED_IN_USER_TOKENS))
            logger.info("BLOCKED_USER_TOKENS: " + str(BLOCKED_USER_TOKENS))
            if token in LOGGED_IN_USER_TOKENS.values():
                return make_response(
                    jsonify(msg="Token valid"),
                    200,
                )
            raise ValueError
        except ValueError as e:
            logger.error(e)
            return make_response(jsonify(msg="Token invalid"), 401)
