#!/usr/bin/python3
"""Create a new view for Place objects that handles all default RESTFul API actions:"""
from flask import abort, jsonify, make_response, request
from models.city import City
from models.places import Place
from api.v1.views import app_views
from models import storage


@app_views.route('/api/v1/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
    def get_places(city_id):
        city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

