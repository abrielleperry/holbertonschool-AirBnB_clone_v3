#!/usr/bin/python3
"""Create a new view for State objects that handles all default
RESTful API actions"""
from flask import abort, jsonify, make_response, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves list all state objects"""
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_id_state(state_id):
    """Retrieves state object by id"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    else:
        return jsonify(state_obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """Creates a state"""
    response = request.get_json()

    if not response:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in response:
        return make_response(jsonify({"error": "Missing name"}), 400)

    created_state = State(**response)
    created_state.save()
    return make_response(jsonify(created_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def put_state(state_id):
    """Updates a state object"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)

    response = request.get_json()

    if not response:
        abort(400, description="Not a JSON")

    # Ignore keys: id, created_at, and updated_at
    keys_to_ignore = ["id", "created_at", "updated_at"]
    for key, value in response.items():
        if key not in keys_to_ignore:
            setattr(state_obj, key, value)

    storage.save()
    return make_response(jsonify(state_obj.to_dict()), 200)
