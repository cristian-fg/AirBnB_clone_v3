#!/usr/bin/python3
""" States views """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', defaults={'state_id': '1'}, strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_object(state_id):
    """Retrieve all objects"""
    data = storage.all("State")
    obj = 'State' + '.' + state_id

    if state_id == '1':
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


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def Delete_object(state_id):
    """Retrieve all objects"""
    data = storage.all('State')
    obj = 'State' + '.' + state_id
    if obj in data:
        storage.delete(data[obj])
        storage.save()
        return (jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def Create_object():
    """ Creates an Object """
    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in data:
        return (jsonify({'error': 'Missing name'}), 400)

    MyState = State(**data)
    storage.new(MyState)
    storage.save()
    return (jsonify(MyState.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def Update_object(state_id):
    """ Updates Object """
    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    MyVar = storage.all('State')
    obj = 'State' + '.' + state_id
    if obj in MyVar:
        for k, v in data.items():
            if k != 'id' or k != 'created_at' or k != 'updated_at':
                setattr(MyVar[obj], k, v)
        storage.save()
        return (jsonify(MyVar[obj].to_dict()), 200)
    else:
        return abort(404)
