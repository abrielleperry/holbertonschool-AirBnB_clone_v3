#!/usr/bin/python3
""" objects that handles all default RestFul API actions for amenities """
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/api/v1/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves list all state objects"""
    amenities = Amenity.query.all()
    amenity_list = [amenity.to_dict()
                    for amenity in amenities]
    return jsonify(amenity_list)


@app_views.route('/api/v1/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/api/v1/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    return jsonify({}), 200


@app_views.route("/api/v1/amenities",
                 methods=["POST"], strict_slashes=False)
def post_amenity(amenity_id):
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    amenity = Amenity(**response)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/api/v1/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def put_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
