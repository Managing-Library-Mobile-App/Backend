import json
import os

from flask import Flask, jsonify
import flask_sqlalchemy
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint