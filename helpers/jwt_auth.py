import os

import jwt
from flask import Response
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from helpers.blocklist import BLOCKED_USER_TOKENS, LOGGED_IN_USER_TOKENS


def verify_jwt_token() -> None | str:
    """
    Verify JWT Token for endpoint
    :returns: response to show if token is invalid or email if valid
    :rtype: Response | str
    """
    try:
        data: tuple[dict, dict] | None = verify_jwt_in_request(optional=True)
        if data:
            jwt_header, jwt_data = data
        else:
            raise ValueError
        token: str = jwt.encode(
            payload=jwt_data,
            key=os.environ.get("JWT_SECRET_KEY"),
            algorithm="HS256",
            headers=jwt_header,
        )
        email: str = get_jwt_identity()
        if email in LOGGED_IN_USER_TOKENS.keys() and (
            email not in BLOCKED_USER_TOKENS.keys()
            or token not in BLOCKED_USER_TOKENS[email]
        ):
            return email
        raise ValueError
    except (
        ValueError,
        jwt.exceptions.ExpiredSignatureError,
        jwt.exceptions.DecodeError,
    ):
        return None
