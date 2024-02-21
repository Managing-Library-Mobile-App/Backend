import flask_restful

from api.available_versions import AvailableVersions
from api.available_routes import AvailableRoutes
from api.favicon import Favicon
from api.account.change_password import ChangePassword
from api.account.delete_account import DeleteAccount
from api.account.login import Login
from api.account.already_logged_in import CheckAlreadyLoggedIn
from api.account.logout import Logout
from api.account.register import Register
from api.data.other.error import (
    ErrorGet,
    ErrorDelete,
    ErrorAdd,
)


def api_add_resources_v1(api: flask_restful.Api) -> None:
    api_without_version = "/api/"
    account = "account/"
    data = "data/"

    # additional
    api.add_resource(
        Favicon,
        "/favicon.ico",
        endpoint="favicon",
    )
    api.add_resource(
        AvailableRoutes,
        f"{api_without_version}available_routes",
        endpoint="available_routes",
    )
    api.add_resource(
        AvailableVersions,
        f"{api_without_version}available_versions",
        endpoint="available_versions",
    )

    # account
    api.add_resource(
        Login,
        f"{api_without_version}{account}login",
        endpoint="login",
    )
    api.add_resource(
        Register,
        f"{api_without_version}{account}register",
        endpoint="register",
    )

    api.add_resource(
        ChangePassword,
        f"{api_without_version}{account}change_password",
        endpoint="change_password",
    )
    api.add_resource(
        DeleteAccount,
        f"{api_without_version}{account}delete_account",
        endpoint="delete_account",
    )
    api.add_resource(
        Logout,
        f"{api_without_version}{account}logout",
        endpoint="logout",
    )

    api.add_resource(
        CheckAlreadyLoggedIn,
        f"{api_without_version}{account}check_login",
        endpoint="check_login",
    )

    # author

    # book

    # book announcement

    # error
    api.add_resource(
        ErrorAdd,
        f"{api_without_version}{data}error_add",
        endpoint="error_add",
    )
    api.add_resource(
        ErrorGet,
        f"{api_without_version}{data}error_get",
        endpoint="error_get",
    )
    api.add_resource(
        ErrorDelete,
        f"{api_without_version}{data}error_delete",
        endpoint="error_delete",
    )

    # library

    # opinion

    # user

    # admin
