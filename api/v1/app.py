#!/usr/bin/python3
"""API"""
import os
from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """closes storage on teardown"""
    return storage.close()


@app.errorhandler(404)
def not_found(error):
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
