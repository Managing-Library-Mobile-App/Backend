from flask import render_template

from imports import *
from __main__ import app
from __main__ import api


@app.route('/debug_toolbar')
def form():
    return "<html><body></body></html>"


