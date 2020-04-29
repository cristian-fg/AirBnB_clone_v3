#!/usr/bin/python3
""" States views """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def retrieve_all_objects():
    """Retrieve all objects"""
    data = storage.all("State")
    new_list = []
    for v in data.values():
        new_list.append(v.to_dict())
    return jsonify(new_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def retrieve_object(state_id):
    """Retrieve all objects"""
    data = storage.all("State")
    for k, v in data.items():
        if state_id in k:
            return jsonify(v.to_dict())
    return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def Delete_object(state_id):
    """Retrieve all objects"""
    data = storage.get('State', state_id)
    if data is None:
        return (abort(404))
    else:
        storage.delete(data)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/states/', methods=['POST'])
def Create_object():
    """ Creates an Object """
    data = request.get_json()
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if data.get('name') is None:
        return (jsonify({'error': 'Missing name'}), 400)
    MyState = State(**data)
    storage.new()
    MyState.save()
    return (jsonify(MyState.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def Update_object(state_id):
    """ Updates Object """
    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)
    MyVar = storage.get('State', state_id)
    if MyVar is None:
        return abort(404)
    for k, v in data.items():
        if k != 'id' or k != 'created_at' or k != 'updated_at':
            setattr(MyVar, k, v)
    storage.save()
    return (jsonify(MyVar.to_dict()), 200)
