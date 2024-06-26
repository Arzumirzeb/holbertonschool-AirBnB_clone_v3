#!/usr/bin/python3

"""first endpoint (route) will be to return the status of your API"""

from flask import Flask
from api.v1.views import app_views
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exc):
    storage.close()


cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def error(error):
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
