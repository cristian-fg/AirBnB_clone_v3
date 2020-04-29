#!/usr/bin/python3
""" Amenity views """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', defaults={'amenity_id': '1'},
                 strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_all_amenities(amenity_id):
    """Retrieve all objects"""
    data = storage.all('Amenity')
    obj = 'Amenity' + '.' + amenity_id

    if amenity_id == '1':
        new_list = []
        for v in data.values():
            new_list.append(v.to_dict())
        return jsonify(new_list)

    elif obj not in data.keys():
        return abort(404)

    else:
        for k, v in data.items():
            if obj in k:
                return jsonify(v.to_dict())
        return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def Delete_amenity(amenity_id):
    """Retrieve all objects"""
    data = storage.all('Amenity')
    obj = 'Amenity' + '.' + amenity_id
    if obj in data:
        storage.delete(data[obj])
        storage.save()
        return (jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def Create_amenity():
    """ Creates an Object """
    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in data:
        return (jsonify({'error': 'Missing name'}), 400)

    MyAmenity = Amenity(**data)
    storage.new(MyAmenity)
    storage.save()
    return (jsonify(MyAmenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def Update_amenity(amenity_id):
    """ Updates Object """
    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    MyVar = storage.all('Amenity')
    obj = 'Amenity' + '.' + amenity_id
    if obj in MyVar:
        for k, v in data.items():
            if k != 'id' or k != 'created_at' or k != 'updated_at':
                setattr(MyVar[obj], k, v)
        storage.save()
        return (jsonify(MyVar[obj].to_dict()), 200)
    else:
        return abort(404)
