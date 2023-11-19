#!/usr/bin/python3
"""Create a new view for State objects tha handles all default
RESTful API actions"""
from flask import abort, jsonify, make_response, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states(self, state_id=None):
    """Retrieves list all state objects"""
    if state_id is None:
        states = storage.all(State).values()
        states_list = [state.to_dict() for state in states]
        return jsonify(states_list)
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())

