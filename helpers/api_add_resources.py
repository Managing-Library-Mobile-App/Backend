import flask_restful
from static.resources import RESOURCES


def api_add_resources(api: flask_restful.Api) -> None:
    """
    Register endpoints for app
    :returns: None
    :rtype: None
    :raises ValueError: Token invalid
    :raises Exception: Token invalid in unknown way
    """
    [api.add_resource(URL, RESOURCES[URL]) for URL in RESOURCES.keys()]
