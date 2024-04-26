#!/usr/bin/python3
'''code of State'''

from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_of_all_state():
    states = storage.all("State")
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_obj(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    state = request.get_json(silent=True)
    if state is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in state.keys():
        return jsonify({"error": "Missing name"}), 400
    new_state = State(name=state['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    states = request.get_json(silent=True)
    the_id = storage.get(State, state_id)
    if states is None:
        return jsonify({"error": "Not a JSON"}), 400
    if the_id is None:
        return abort(404)
    for key, value in states.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
