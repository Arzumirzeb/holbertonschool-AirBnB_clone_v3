#!/usr/bin/python3
'''code of City'''

from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def delete_obj(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_obj(state_id):
    city = storage.get(City, state_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    data['state_id'] = state_id
    new_state = City(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(state_id):
    data = request.get_json(silent=True)
    the_id = storage.get(City, state_id)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if the_id is None:
        return abort(404)
    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(the_id, key, value)
    storage.save()
    return jsonify(the_id.to_dict()), 200
