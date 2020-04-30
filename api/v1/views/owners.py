#!/usr/bin/python3
""" owners views """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.owner import Owner


@app_views.route('/owners', defaults={'owner_id': '1'}, strict_slashes=False)
@app_views.route('/owners/<owner_id>', methods=['GET'], strict_slashes=False)
def retrieve_owners(owner_id):
    """Retrieve all objects"""
    data = storage.all('Owner')
    obj = 'Owner' + '.' + owner_id

    if owner_id == '1':
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


@app_views.route('/owners/<owner_id>', methods=['DELETE'],
                 strict_slashes=False)
def Delete_owner(owner_id):
    """Retrieve all objects"""
    data = storage.all('Owner')
    obj = 'Owner' + '.' + owner_id
    if obj in data:
        storage.delete(data[obj])
        storage.save()
        return (jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/owners', methods=['POST'], strict_slashes=False)
def Create_owner():
    """ Creates an Object """
    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if 'first_name' not in data:
        return (jsonify({'error': 'Missing first_name'}), 400)

    if 'last_name' not in data:
        return (jsonify({'error': 'Missing last_name'}), 400)

    Myowner = Owner(**data)
    storage.new(Myowner)
    storage.save()
    return (jsonify(Myowner.to_dict()), 201)


@app_views.route('/owners/<owner_id>', methods=['PUT'], strict_slashes=False)
def Update_owner(owner_id):
    """ Updates Object """
    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    MyVar = storage.all('Owner')
    obj = 'Owner' + '.' + owner_id
    if obj in MyVar:
        for k, v in data.items():
            if k != 'id' or k != 'created_at' or k != 'updated_at':
                setattr(MyVar[obj], k, v)
        storage.save()
        return (jsonify(MyVar[obj].to_dict()), 200)
    else:
        return abort(404)
