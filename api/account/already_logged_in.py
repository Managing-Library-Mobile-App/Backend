from __future__ import annotations

from flask import Response, jsonify, make_response, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_restful import Resource
from loguru import logger

from api.account.blocklist import BLOCK_LIST_USERS, BLOCK_LIST_TOKENS


class CheckAlreadyLoggedIn(Resource):
    def __init__(self) -> None:
        super(CheckAlreadyLoggedIn, self).__init__()

    def get(self) -> Response:
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            auth: str | None = request.headers.get("Authorization")
            token: str = ""
            if auth:
                token = auth.split(" ")[1]
            logger.info(token)
            logger.info(BLOCK_LIST_USERS)
            logger.info(BLOCK_LIST_TOKENS)
            if current_user not in BLOCK_LIST_USERS:
                if token not in BLOCK_LIST_TOKENS:
                    BLOCK_LIST_USERS.add(current_user)
                    BLOCK_LIST_TOKENS.add(token)
                    return make_response(
                        jsonify(
                            logged_in_as=current_user, message="User just logged in"
                        ),
                        200,
                    )
                return make_response(
                    jsonify(logged_in_as=None, message="Token invalid"),
                    200,
                )

            logger.info(BLOCK_LIST_USERS)
            logger.info(BLOCK_LIST_TOKENS)
            return make_response(
                jsonify(logged_in_as=current_user, message="User already logged in"),
                200,
            )
        except AttributeError as e:
            logger.error(e)
            return make_response(
                jsonify(already_logged_in_as=None, message="User not logged in"), 401
            )
