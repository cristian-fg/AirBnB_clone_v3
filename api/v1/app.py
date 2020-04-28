#!/usr/bin/python3
"""Status API """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def SessionClose(self):
    """ close session"""
    storage.close()


if __name__ == "__main__":
    ht = getenv('HBNB_API_HOST', '0.0.0.0')
    pt = getenv('HBNB_API_HOST', '5000')
    app.run(debug=True, host=ht, port=pt, threaded=True)
