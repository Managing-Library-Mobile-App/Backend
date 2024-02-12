import flask_restful

from routes.additional.available_versions import AvailableVersions
from routes.additional.available_routes import AvailableRoutes
from routes.additional.favicon import Favicon
from routes.v1.account.change_password import ChangePassword
from routes.v1.account.delete_account import DeleteAccount
from routes.v1.account.login import Login
from routes.v1.account.logout import Logout
from routes.v1.account.register import Register
from routes.v1.data.other.error import (
    ErrorGet,
    ErrorDelete,
    ErrorAdd,
)


def api_add_resources_v1(api: flask_restful.Api) -> None:
    api_version = "/api/v1/"
    api_without_version = "/api/"

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
        f"{api_version}login",
        endpoint="login",
    )
    api.add_resource(
        Register,
        f"{api_version}register",
        endpoint="register",
    )

    api.add_resource(
        ChangePassword,
        f"{api_version}change_password",
        endpoint="change_password",
    )
    api.add_resource(
        DeleteAccount,
        f"{api_version}delete_account",
        endpoint="delete_account",
    )
    api.add_resource(
        Logout,
        f"{api_version}logout",
        endpoint="logout",
    )

    # author

    # book

    # book announcement

    # error
    api.add_resource(
        ErrorAdd,
        f"{api_version}error_add",
        endpoint="error_add",
    )
    api.add_resource(
        ErrorGet,
        f"{api_version}error_get",
        endpoint="error_get",
    )
    api.add_resource(
        ErrorDelete,
        f"{api_version}error_delete",
        endpoint="error_delete",
    )

    # library

    # opinion

    # user

    # admin
