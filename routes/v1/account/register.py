import re
import string

from flask_restful import reqparse  # type: ignore
from loguru import logger
from flasgger import swag_from
from flask_restful import Resource


class User:
    active: bool = False

    def __init__(self, username, password, email=None) -> None:
        self.username = username
        self.password = password
        self.email = email


def contains_special_char(characters: str) -> bool:
    for character in characters:
        if character in string.punctuation:
            return True
    return False


def contains_illegal_char(characters: str) -> bool:
    if characters.__contains__(" "):
        return True
    return False


def contains_uppercase_char(characters: str) -> bool:
    if characters.lower() == characters:
        return False
    return True


def authenticate_register_credentials(
    username: str, password: str, email: str
) -> dict[str, str | None | User]:
    if contains_illegal_char(username):
        return {
            "user": None,
            "message": "contains_illegal_char_username",
            "details": "Illegal characters in username such as space",
        }
    if not contains_special_char(password):
        return {
            "user": None,
            "message": "not_contains_special_char_password",
            "details": "No special characters in password. Required at least one",
        }
    if contains_illegal_char(password):
        return {
            "user": None,
            "message": "contains_illegal_char_password",
            "details": "Illegal characters in password such as space",
        }
    if not contains_uppercase_char(password):
        return {
            "user": None,
            "message": "not_contains_uppercase_char_password",
            "details": "Password has no uppercase letters. Required at least one.",
        }
    if len(username) < 10:
        return {
            "user": None,
            "message": "username_too_short",
            "details": "Username should have a minimum of 10 characters",
        }
    if len(username) > 50:
        return {
            "user": None,
            "message": "username_too_long",
            "details": "Username should have 50 characters max",
        }
    if len(password) < 10:
        return {
            "user": None,
            "message": "password_too_short",
            "details": "Password should have a minimum of 10 characters",
        }
    if len(password) > 50:
        return {
            "user": None,
            "message": "password_too_long",
            "details": "Passwrod should have 50 characters max",
        }
    if len(email) > 50:
        return {
            "user": None,
            "message": "email_too_long",
            "details": "Email should have 50 characters max",
        }
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(regex, email):
        return {
            "user": None,
            "message": "email_of_wrong_format",
            "details": "User already exists",
        }
    # TODO faktyczna weryfikacja użytkowników, którzy są w bazie
    if username == "Admin-1234":
        return {
            "user": None,
            "message": "user_already_exists",
            "details": "User already exists",
        }
    user = User(username=username, password=password, email=email)
    return {
        "user": user,
        "message": "register_successful",
        "details": "Register successful",
    }


class Register(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            location="json",
        )
        self.reqparse.add_argument("password", type=str, required=True, location="json")
        self.reqparse.add_argument("email", type=str, required=True, location="json")
        super(Register, self).__init__()

    @swag_from("login_swagger.yml")
    def post(self) -> dict[str, None | str | bool]:
        args = self.reqparse.parse_args()
        username = args.get("username")
        password = args.get("password")
        email = args.get("email")
        registration_output = authenticate_register(username, password, email)
        if isinstance(registration_output["user"], User):
            logger.info(
                f"Zarejestrowano użytkownika {registration_output['user'].username}"
            )
            return {
                "registered": True,
                "message": str(registration_output["message"]),
                "details": str(registration_output["details"]),
            }
        logger.info(
            f"Nieudana próba rejestracji użytkownika. {registration_output['message']}"
        )
        return {
            "registered": False,
            "message": str(registration_output["message"]),
            "details": str(registration_output["details"]),
        }


def authenticate_register(username, password, email) -> dict[str, None | str | User]:
    register_data = authenticate_register_credentials(
        username=username, password=password, email=email
    )
    return register_data
