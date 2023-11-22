#!/usr/bin/python3
"""Create a new view for Place obj that handles all RESTFul API actions:"""
from flask import jsonify, make_response, abort, request
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = [place.to_dict() for place in city.places]
    return jsonify(all_places)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req_data = request.get_json(silent=True)
    if req_data is None:
        return abort(400, jsonify({"error": "Not a JSON"}))
    if 'user_id' not in req_data:
        return abort(400, jsonify({"error": "Missing user_id"}))
    user = storage.get(User, req_datadata['user_id'])
    if user is None:
        abort(404)
    if 'name' not in req_data:
        return abort(400, jsonify({"error": "Missing name"}))
    req_data['city_id'] = city_id
    print(req_data)
    post_place = Place(**req_data)
    storage.save()
    return make_response(jsonify(post_place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    req_data = request.get_json()
    if req_data is None:
        abort(400, "Not a JSON")
    for key, value in req_data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place_obj, key, value)
    storage.save()
    return jsonify(place_obj.to_dict()), 200
