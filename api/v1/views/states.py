#!/usr/bin/python3
""" States views """
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage

@app_views.route('/states', methods=['GET'])
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
    data = storage.all('State')
    obj = 'State' + '.' + state_id
    for k in data.keys():
        if obj in k:
            storage.delete(data[obj])
            storage.save()
            return jsonify({}), 200
    return abort(404)
