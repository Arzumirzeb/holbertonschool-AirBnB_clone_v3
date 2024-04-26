#!/usr/bin/python3
'''code of State'''
from os import abort
from flask import jsonify, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)
def list_of_all_state():
    states = storage.all("States")
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/api/v1/states/<state_id>', methods=['GET'])
def get_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_obj(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states/', methods=['POST'], strict_slashes=False)
def create_state():
    state = request.get_json()
    if state is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in state.keys():
        return jsonify({"error": "Missing name"}), 400
    new_state = State(name=state['name'])
    state.new(new_state)
    state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = request.get_json()
    the_id = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not a JSON"}), 400
    if the_id is None:
        return abort(404)
    for key, value in state.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
