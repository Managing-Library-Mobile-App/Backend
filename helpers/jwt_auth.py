import os

import jwt
from flask import jsonify, Response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from loguru import logger

from helpers.blocklist import BLOCKED_USER_TOKENS, LOGGED_IN_USER_TOKENS


def verify_jwt_token() -> Response | str:
    """
    Verify JWT Token for endpoint
    :returns: response to show if token is invalid or email if valid
    :rtype: Response | str
    """
    try:
        data = verify_jwt_in_request(optional=True)
        logger.info(data)
        if data:
            jwt_header, jwt_data = data
        else:
            raise ValueError
        token = jwt.encode(
            payload=jwt_data,
            key=os.environ.get("JWT_SECRET_KEY"),
            algorithm="HS256",
            headers=jwt_header,
        )
        email = get_jwt_identity()
        logger.info(email)
        if email in LOGGED_IN_USER_TOKENS.keys() and (
            email not in BLOCKED_USER_TOKENS.keys()
            or token not in BLOCKED_USER_TOKENS[email]
        ):
            return email
        raise ValueError
    except ValueError:
        return jsonify(
            msg="Token invalid",
        )
    except Exception:
        return jsonify(
            msg="Token invalid",
        )
