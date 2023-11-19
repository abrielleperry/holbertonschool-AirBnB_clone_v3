#!/usr/bin/python3
"""Create a new view for State objects tha handles all default
RESTful API actions"""
from flask import abort, jsonify, make_response, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves list all state objects"""
    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states(state_id):
    """Retrieves state object by id"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route("/states", methods=["DELETE"], strict_slashes=False)
def delete_state(self, state_id):
    """Deletes a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)
