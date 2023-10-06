# Backend
Written in Flask


def figure_error(message):
    print(message)
    response = jsonify({"message": message})
    response.status_code = 404
    return response

