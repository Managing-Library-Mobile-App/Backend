# Backend
Written in Flask


def figure_error(message):
    print(message)
    response = jsonify({"message": message})
    response.status_code = 404
    return response



google books API
open library APIs - najlepsze bo ma wszystko
python openlibrary-client
book search API
Authors API
Covers API
