#!/usr/bin/python3
'''code of User'''

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    users = storage.all("User")
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users_with_id(user_id):
    user = storage.get(User, user_id)
    if user is None:
        return {"error": "Not found"}, 404
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_users(user_id):
    user = storage.get(User, user_id)
    if user is None:
        return {"error": "Not found"}, 404
    storage.delete(user)
    storage.save()
    return {}, 200


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def post_users():
    data = request.get_json(silent=True)
    if data is None:
        return {"error": "Not a JSON"}, 400
    if "email" not in data.keys():
        return {"error": "Missing email"}, 400
    if "password" not in data.keys():
        return {"error": "Missing password"}, 400
    users = User(**data)
    storage.new(users)
    storage.save()
    return jsonify(users.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_users(user_id):
    data = request.get_json(silent=True)
    user = storage.get(User, user_id)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if user is None:
        return abort(404)
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return user.to_dict(), 200
