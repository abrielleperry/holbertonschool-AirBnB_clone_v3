#!/usr/bin/python3
"""index"""
from flask import Flask, jsonify
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/status")
def status():
    response = {"status": "OK"}
    return jsonify(response)

@app_views.route("stats")
def stats():
    """Retrieves the number of objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    object_name = ["amenities", "cities", "places", "reviews", "states", "users"]

    stats = {}
    for object in range(len(classes)):
        stats[object_name[object]] = storage.count(classes[object])
    return jsonify(stats)