#!/usr/bin/python3
'''code of City'''

from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.state import City


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def list_of_all_city():
    cities = storage.all("City")
    return jsonify([state.to_dict() for state in cities.values()])


@app_views.route('/cities/<state_id>', methods=['GET'], strict_slashes=False)
def get_id(state_id):
    state = storage.get(City, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


@app_views.route('/cities/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_obj(state_id):
    state = storage.get(City, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/', methods=['POST'], strict_slashes=False)
def create_city():
    state = request.get_json(silent=True)
    if state is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in state.keys():
        return jsonify({"error": "Missing name"}), 400
    new_state = City(name=state['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/cities/<state_id>', methods=['PUT'], strict_slashes=False)
def update_city(state_id):
    data = request.get_json(silent=True)
    the_id = storage.get(City, state_id)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if the_id is None:
        return abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(the_id, key, value)
    storage.save()
    return jsonify(the_id.to_dict()), 200
