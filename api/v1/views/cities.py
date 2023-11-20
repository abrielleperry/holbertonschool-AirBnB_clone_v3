from flask import abort, jsonify, make_response, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    list_of_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_of_cities)

@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route("/cities/<city_id>/", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def post_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    response = request.get_json()
    if not response:
        abort(404, description="Not a JSON")

    if "name" not in response:
        return make_response(jsonify({"error": "Missing name"}), 400)

    created_city = City(**response)
    created_city.state_id = state_id
    created_city.save()
    return make_response(jsonify(created_city.to_dict()), 201)

@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)

    response = request.get_json()
    if not response:
        abort(400, description="Not a JSON")

    keys_to_ignore = ["id", "state_id", "created_at", "updated_at"]
    for key, value in response.items():
        if key not in keys_to_ignore:
            setattr(city_obj, key, value)

    storage.save()
    return make_response(jsonify(city_obj.to_dict()), 200)
