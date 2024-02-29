from __future__ import annotations

import os

import jwt
from flask import jsonify, Response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from helpers.blocklist import BLOCK_LIST_USERS, BLOCK_LIST_TOKENS


def verify_jwt_token() -> Response | str:
    try:
        data = verify_jwt_in_request()
        if data:
            jwt_header, jwt_data = data
        else:
            raise AttributeError
        token = jwt.encode(
            payload=jwt_data,
            key=os.environ.get("JWT_SECRET_KEY"),
            algorithm="HS256",
            headers=jwt_header,
        )
        email = get_jwt_identity()
        if email not in BLOCK_LIST_USERS or token not in BLOCK_LIST_TOKENS:
            raise AttributeError
    except AttributeError:
        return jsonify(
            password_changed=False,
            message="user_not_logged_in",
            details="User not logged in (No session)",
        )
    return email
