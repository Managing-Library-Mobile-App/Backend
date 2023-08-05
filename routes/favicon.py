from flask import send_from_directory

from imports import *
from __main__ import app
from __main__ import api

from flask import url_for


# Load Browser Favorite Icon
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')
