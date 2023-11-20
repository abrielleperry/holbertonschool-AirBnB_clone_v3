#!/usr/bin/python3
""" objects that handles all default RestFul API actions for amenities """
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/api/v1/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves list all state objects"""
    amenity_list = [amenity.to_dict() for amenity in storage.all]
    return jsonify(amenity_list)


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/api/v1/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/api/v1/amenities",
                 methods=["POST"], strict_slashes=False)
def post_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    response = request.get_json()
    if not response:
        abort(400, description="Not a JSON")

    if "name" not in response:
        return make_response(jsonify({"error": "Missing name"}), 400)

    created_amenity = Amenity(**response)
    created_amenity.amenity_id = amenity_id
    created_amenity.save()
    return make_response(jsonify(created_city.to_dict()), 201)


@app_views.route("/api/v1/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def put_amenity(amenity_id):
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)

    response = request.get_json()
    if not response:
        abort(400, description="Not a JSON")

    keys_to_ignore = ["id", "created_at", "updated_at"]
    for key, value in response.items():
        if key not in keys_to_ignore:
            setattr(amenity_obj, key, value)

    storage.save()
    return make_response(jsonify(amenity_obj.to_dict()), 200)
