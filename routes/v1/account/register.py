import re
import string

from flask_restful import reqparse  # type: ignore
from loguru import logger
from flasgger import swag_from
from flask_restful import Resource


class User:
    active: bool = False

    def __init__(self, username, password, email):
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
    if characters.lower() == characters.upper():
        return False
    return True


def authenticate_register_credentials(
    username: str, password: str, email: str
) -> User | dict[str, str]:
    if contains_illegal_char(username):
        return {
            "user": None,
            "message": "username_illegal_chars",
            "details": "Illegal characters in username such as space",
        }
    if not contains_special_char(password):
        return {
            "user": None,
            "message": "password_no_special_chars",
            "details": "No special characters in password. Required at least one",
        }
    if contains_illegal_char(password):
        return {
            "user": None,
            "message": "password_illegal_chars",
            "details": "Illegal characters in password such as space",
        }
    if not contains_uppercase_char(password):
        return {
            "user": None,
            "message": "password_no_uppercase_char",
            "details": "Password has no uppercase letters. Required at least one.",
        }
    if len(username) < 10:
        return {
            "user": None,
            "message": "username_too_short",
            "details": "Minimum of 10 characters",
        }
    if len(username) > 50:
        return {
            "user": None,
            "message": "username_too_long",
            "details": "Max 50 characters",
        }
    if len(password) < 10:
        return {
            "user": None,
            "message": "password_too_short",
            "details": "Minimum of 10 characters",
        }
    if len(password) > 50:
        return {
            "user": None,
            "message": "password_too_long",
            "details": "Max 50 characters",
        }
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(regex, email):
        return {
            "user": None,
            "message": "email_of_wrong_format",
            "details": "User already exists",
        }
    # TODO faktyczna weryfikacja użytkowników, którzy są w bazie
    if username == "admin":
        return {
            "user": None,
            "message": "user_already_exists",
            "details": "User already exists",
        }
    user = User(username=username, password=password, email=email)
    return {
        "user": user,
        "message": "user_already_exists",
        "details": "User already exists",
    }


class Register(Resource):
    def __init__(self):
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
    def get(self):
        args = self.reqparse.parse_args()
        username = args.get("username")
        password = args.get("password")
        email = args.get("email")
        registration_output = authenticate_register(username, password, email)
        if registration_output["user"] is not None:
            logger.info(
                f"Zarejestrowano użytkownika {registration_output['user'].username}"
            )
            return {"registered": True}
        logger.info(
            f"Nieudana próba rejestracji użytkownika. {registration_output['message']}"
        )
        return {
            "registered": False,
            "message": registration_output["message"],
            "details": registration_output["details"],
        }


def authenticate_register(username, password, email):
    register_data = authenticate_register_credentials(
        username=username, password=password, email=email
    )
    if register_data["user"] is not None:
        return {"user": register_data["user"]}
    return register_data
