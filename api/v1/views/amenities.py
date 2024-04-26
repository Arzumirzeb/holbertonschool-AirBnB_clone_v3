#!/usr/bin/python3
'''code of Amenity'''

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity():
    amenities = storage.all("Amenity")
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_with_id(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return {"error": "Not found"}, 404
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return {"error": "Not found"}, 404
    storage.delete(amenity)
    storage.save()
    return {}, 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity(state_id):
    data = request.get_json(silent=True)
    if data is None:
        return {"error": "Not a JSON"}, 400
    if "name" not in data:
        return {"error": "Missing name"}, 400
    data['state_id'] = state_id
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    data = request.get_json(silent=True)
    amenity = storage.get(Amenity, amenity_id)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if amenity is None:
        return abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return amenity.to_dict(), 200
