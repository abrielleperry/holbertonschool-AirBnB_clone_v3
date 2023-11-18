#!/usr/bin/python3
"""index"""
from flask import Flask

app = Flask(__name__)

@app_views.route("/status")
from api.v1.views import app_views
def status():
  response = {"status": "OK"}
  return jsonify(response)
