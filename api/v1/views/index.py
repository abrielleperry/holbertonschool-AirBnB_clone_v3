#!/usr/bin/python3
"""index"""
from flask import Flask, jsonify
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/status")
def status():
    response = {"status": "OK"}
    return jsonify(response)
