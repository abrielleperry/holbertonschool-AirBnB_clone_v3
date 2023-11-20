#!/usr/bin/python3
""" objects that handles all default RestFul API actions for amenities """
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves list all state objects"""
    amenity_list = [amenity.to_dict()
                    for amenity in storage.all(Amenity).values()]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    one_amenity = storage.get(Amenity, amenity_id)
    if one_amenity is None:
        abort(404)
    return jsonify(one_amenity.to_dict())


@app_views.route("/api/v1/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    one_amenity = storage.get(Amenity, amenity_id)
    if one_amenity is None:
        abort(404)
    storage.delete(one_amenity)
    storage.save()
    return jsonify({}), 200)


@app_views.route("/api/v1/amenities",
                 methods=["POST"], strict_slashes=False)
def post_amenity(amenity_id):
    get_data = request.get_json()
    if get_data is None:
        abort(400, "Not a JSON")
    if "name" not in get_data"
        abort(400, "Missing name")
    response = request.get_json()

    created_amenity = Amenity(**response)
    storage.new = created_amenity
    storage.save()
    return jsonify(created_amenity.to_dict()), 201)


@app_views.route("/api/v1/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def put_amenity(amenity_id):
    one_amenity = storage.get(Amenity, amenity_id)
    if one_amenity_ is None:
        abort(404)
    response = request.get_json()
    if not one_amenity:
        abort(400, "Not a JSON")

    keys_to_ignore = ["id", "created_at", "updated_at"]
    for key, value in response.items():
        if key not in keys_to_ignore:
            setattr(one_amenity, key, value)

    storage.save()
    return jsonify(one_amenity).to_dict(), 200
