#!/usr/bin/python3
""" Index File """
from api.v1.views import app_views
from flask import jsonify
from api.v1 import app


@app_views.route('/status')
def status():
    """My status """
    return jsonify({"status": "OK"})
