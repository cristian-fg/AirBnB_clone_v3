#!/usr/bin/python3
""" Index File """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """My status """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ shows status """
    count = {
        "amenities": storage.count("Amenity"), 
        "cities": storage.count("City"), 
        "places": storage.count("Place"), 
        "reviews": storage.count("Review"), 
        "states": storage.count("State"), 
        "users": storage.count("User")
    }
    return jsonify(count)

