from imports import *
from __main__ import app
from __main__ import api


# Wyświetlenie wszystkich endpointów
def routes_list():
    api_hidden_routes = ["/static/<path:filename>",
                         "/swagger.json",
                         "/swagger/<path:path>",
                         "/swagger/dist/<path:filename>"]
    api_routes = []
    for endpoint in app.url_map.iter_rules():
        methods = ','.join(endpoint.methods)
        if endpoint.rule not in api_hidden_routes:
            api_routes.append({
                'endpoint': str(endpoint),
                'methods': methods
            })
    sorted_api_routes = sorted(api_routes, key=lambda k: k['endpoint'])
    return sorted_api_routes


class available_routes(Resource):
    def get(self):
        return jsonify(routes_list())


api.add_resource(available_routes, '/', '/available_routes')
