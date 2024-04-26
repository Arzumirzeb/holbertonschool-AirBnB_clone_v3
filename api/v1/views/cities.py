#!/usr/bin/python3
'''code of City'''

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_with_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return {"error": "Not found"}, 404
    return [city.to_dict() for city in state.cities]


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return {"error": "Not found"}, 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return {"error": "Not found"}, 404
    storage.delete(city)
    storage.save()
    return {}, 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return {"error": "Not found"}, 404
    data = request.get_json(silent=True)
    if data is None:
        return {"error": "Not a JSON"}, 400
    if "name" not in data:
        return {"error": "Missing name"}, 400
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    data = request.get_json(silent=True)
    city = storage.get(City, city_id)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if city is None:
        return abort(404)
    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return city.to_dict(), 200
