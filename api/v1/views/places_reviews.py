#!/usr/bin/python3
"""Create a new view for Review object 
that handles all default RESTFul API actions"""

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

@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return make_response(jsonify{}, 200)

@app_views.route('/places/<places_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a Review"""
    