from typing import Any

from flask import make_response, jsonify, Response


def create_response(static_response: (dict[str, Any], int),
                    dynamic_response_data: dict[str, Any] = None) -> Response:
    response_body = static_response[0]
    if dynamic_response_data:
        for key, value in dynamic_response_data.items():
            response_body[key] = value
    status_code = static_response[1]
    return make_response(
        jsonify(response_body), status_code
    )


# Static
PASSWORD_WRONG_FORMAT_RESPONSE: (dict[str, Any], int) = {
    "message": "password_wrong_format",
    "details": """Wrong password format. Password should have from 10 to 50 characters.
                It should contain at least one upper letter, at least 1 lower letter, at least 1 number and
                at least one special character"""
}, 403
PASSWORD_CHANGED_RESPONSE: (dict[str, str], int) = {
    "message": "password_changed",
    "details": "Password changed",
}, 200

PASSWORD_NOT_CHANGED_RESPONSE: (dict[str, str], int) = {
    "message": "wrong_password",
    "details": "Wrong password",
}, 401
TOKEN_INVALID_RESPONSE: (dict[str, str], int) = {
    "message": "token_invalid",
    "details": "Token invalid"
}, 401
TOKEN_VALID_RESPONSE: (dict[str, str], int) = {
    "message": "token_valid",
    "details": "Token valid"
}, 200
CANNOT_DELETE_ADMIN_RESPONSE: (dict[str, str], int) = {
    "message": "cannot_delete_admin",
    "details": "Admin account cannot be deleted",
}, 404

USER_DELETED_RESPONSE: (dict[str, str], int) = {
    "message": "user_deleted",
    "details": "User deleted successfully",
}, 200
USER_DOES_NOT_EXIST_RESPONSE: (dict[str, str], int) = {
    "message": "user_does_not_exist",
    "details": "User does not exist",
}, 404
WRONG_SECRET_RESPONSE: (dict[str, str], int) = {
    "message": "wrong_secret",
    "details": "Wrong secret field value. Cannot view logged in users.",
}, 401
LOGGED_OUT_RESPONSE: (dict[str, str], int) = {
    "message": "logged_out",
    "details": "Logged out"
}, 200
NOT_LOGGED_OUT_RESPONSE: (dict[str, str], int) = {
    "message": "not_logged_out",
    "details": "Could not log out. User was not logged in."
}, 200
USER_NOT_LOGGED_IN_RESPONSE: (dict[str, str], int) = {
    "message": "authentication_failed",
    "details": "Authentication failed. Wrong email or password",
}, 401
LOCKED_USER_LOGIN_ATTEMPTS_RESPONSE: (dict[str, str], int) = {
    "message": "locked_user_login_attempts",
    "details": "User locked because of too many unsuccessful attempts",
}, 401
EMAIL_WRONG_FORMAT_RESPONSE: (dict[str, str], int) = {
    "message": "username_wrong_format",
    "details": "Wrong username format. It should be from 10 to 50 characters "
               "and it can only contain upper letters, lower letters, "
               "numbers and signs: - and _",
}, 401
USER_NOT_FOUND_RESPONSE: (dict[str, str], int) = {
    "message": "user_not_found",
    "details": "User logged in with such token not found"
}, 401
USER_ALREADY_EXISTS_RESPONSE: (dict[str, str], int) = {
    "message": "user_already_exists",
    "details": "User already exists",
}, 401
REGISTER_SUCCESSFUL_RESPONSE: (dict[str, str], int) = {
    "message": "register_successful",
    "details": "Register successful",
}, 200
INSUFFICIENT_PERMISSIONS_RESPONSE: (dict[str, str], int) = {
    "message": "insufficient_permissions",
    "details": "Insufficient permissions. Requires admin or access to the object",
}, 404
OBJECT_CREATED_RESPONSE: (dict[str, str], int) = {
    "message": "object_created",
    "details": "Object created"
}, 200
OBJECT_DELETED_RESPONSE: (dict[str, str], int) = {
    "message": "object_deleted",
    "details": "Object deleted"
}, 200
OBJECT_MODIFIED_RESPONSE: (dict[str, str], int) = {
    "message": "object_modified",
    "details": "Object modified"
}, 200
INVALID_PASSWORD_RESPONSE: (dict[str, str], int) = {
    "message": "invalid_password",
    "details": "Invalid password"
}, 401

# Mutable
USER_OBJECTS_LIST_RESPONSE: (dict[str, Any], int) = {
    "users": None  # Mutable
}, 200
USER_OBJECT_RESPONSE: (dict[str, Any], int) = {
    "user": None  # Mutable
}, 200
OPINION_OBJECTS_LIST_RESPONSE: (dict[str, Any], int) = {
    "opinions": None  # Mutable
}, 200
OPINION_OBJECT_RESPONSE: (dict[str, Any], int) = {
    "opinion": None  # Mutable
}, 200
LIBRARY_OBJECTS_LIST_RESPONSE: (dict[str, Any], int) = {
    "libraries": None  # Mutable
}, 200
LIBRARY_OBJECT_RESPONSE: (dict[str, Any], int) = {
    "library": None  # Mutable
}, 200
BOOK_OBJECTS_LIST_RESPONSE: (dict[str, Any], int) = {
    "books": None  # Mutable
}, 200
BOOK_OBJECT_RESPONSE: (dict[str, Any], int) = {
    "book": None  # Mutable
}, 200
BOOK_ANNOUNCEMENT_OBJECTS_LIST_RESPONSE: (dict[str, Any], int) = {
    "book_announcements": None  # Mutable
}, 200
BOOK_ANNOUNCEMENT_OBJECT_RESPONSE: (dict[str, Any], int) = {
    "book_announcement": None  # Mutable
}, 200
AUTHOR_OBJECTS_LIST_RESPONSE: (dict[str, Any], int) = {
    "authors": None  # Mutable
}, 200
AUTHOR_OBJECT_RESPONSE: (dict[str, Any], int) = {
    "author": None  # Mutable
}, 200
LOGGED_IN_USERS_RESPONSE: (dict[str, Any], int) = {
    "logged_in_users": None  # Mutable
}, 200
ALREADY_LOGGED_IN_RESPONSE: (dict[str, Any], int) = {
    "message": "already_logged_in",
    "details": "Already logged in",
    "token": None  # Mutable
}, 401
LOGIN_SUCCESSFUL_RESPONSE: (dict[str, Any], int) = {
    "message": "login_successful",
    "details": "Login successful",
    "token": None  # Mutable
}, 200
