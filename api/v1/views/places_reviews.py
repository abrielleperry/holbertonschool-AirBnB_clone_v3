#!/usr/bin/python3
"""Create a new view for Review object
that handles all default RESTFul API actions
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = [review.to_dict() for review in storage.all(Review).values() if
               review.place_id == place_id]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return make_response(jsonify{}, 200)


@app_views.route('/places/<places_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    obj_dict = request.get_json()
    if not obj_dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    user_id = obj_dict.get('user_id')
    text = obj_dict.get('text')

    if not user_id:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    if not text:
        return make_response(jsonify({"error": "Missing text"}), 400)

    if not storage.get(User, user_id):
        abort(404)

    obj_dict['place_id'] = place_id
    new_review = Review(**obj_dict)
    new_review.save()

    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    obj_dict = request.get_json()

    if not obj_dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in obj_dict.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    review.save()
    return make_response(jsonify(review.to_dict()), 200)
