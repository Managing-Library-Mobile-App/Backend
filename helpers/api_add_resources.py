import flask_restful

from routes.additional.available_versions import AvailableVersions
from routes.additional.available_routes import AvailableRoutes
from routes.additional.swagger import Swagger
from routes.additional.favicon import Favicon
from routes.v1.account.login import Login
from routes.v1.account.register import Register


def api_add_resources_v1(api: flask_restful.Api) -> None:
    api_version = "/api/v1/"
    api_without_version = "/api/"
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
        AvailableVersions,
        f"{api_without_version}available_versions",
        endpoint="available_versions",
    )
    api.add_resource(
        Swagger,
        f"{api_without_version}swagger",
        endpoint="swagger",
    )
