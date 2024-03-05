from __future__ import annotations

from flask import Response, jsonify, make_response, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_restful import Resource
from loguru import logger

from helpers.blocklist import BLOCK_LIST_USERS, BLOCK_LIST_TOKENS


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
            logger.info("BLOCK_LIST_USERS: " + str(BLOCK_LIST_USERS))
            logger.info("BLOCK_LIST_TOKENS: " + str(BLOCK_LIST_TOKENS))
            if token in BLOCK_LIST_TOKENS and current_user not in BLOCK_LIST_USERS:
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
