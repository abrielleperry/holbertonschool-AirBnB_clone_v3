#!/usr/bin/python3
"""new view for User object that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/api/v1/users', methods=['GET'], strict_slashes=False)
def get_users():
    """retrieves list of all user objects"""
    users = storage.all(User).values()
    users = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users)


@app_views.route('/api/v1/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """retrieves a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user_id.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """creates user"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """updates user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
