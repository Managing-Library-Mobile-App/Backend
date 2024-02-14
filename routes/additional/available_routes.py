from flask import jsonify, current_app
from flask_restful import Resource


def routes_list():
    api_hidden_routes = [
        "/static/",
        "swagger",
        ".help.html",
        ".help.json",
        "/spec",
        "favicon",
    ]
    api_routes = []
    for endpoint in current_app.url_map.iter_rules():
        forbidder_route = False
        methods = ",".join(endpoint.methods)
        for api_hidden_route in api_hidden_routes:
            if api_hidden_route in endpoint.rule:
                forbidder_route = True
                break
        if not forbidder_route:
            api_routes.append({"endpoint": str(endpoint), "methods": methods})
    sorted_api_routes = sorted(api_routes, key=lambda k: k["endpoint"])
    return sorted_api_routes


class AvailableRoutes(Resource):
    def get(self):
        return jsonify(routes_list())
