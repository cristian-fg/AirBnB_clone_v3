#!/usr/bin/python3
"""Status API """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def SessionClose(self):
    """ close session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if getenv('HBNB_API_HOST') and getenv('HBNB_API_PORT'):
        ht = getenv('HBNB_API_HOST')
        pt = getenv('HBNB_API_PORT')
    else:
        ht = '0.0.0.0'
        pt = 5000
    app.run(debug=True, host=ht, port=pt, threaded=True)
