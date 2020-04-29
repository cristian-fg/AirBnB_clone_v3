#!/usr/bin/python3
""" Amenity views """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', defaults={'user_id': '1'},
                 strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_all_users(user_id):
    """Retrieve all objects"""
    data = storage.all('User')
    obj = 'User' + '.' + user_id

    if user_id == '1':
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


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def Delete_user(user_id):
    """Retrieve all objects"""
    data = storage.all('User')
    obj = 'User' + '.' + user_id
    if obj in data:
        storage.delete(data[obj])
        storage.save()
        return (jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def Create_user():
    """ Creates an Object """
    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if 'email' not in data:
        return (jsonify({'error': 'Missing email'}), 400)

    if 'password' not in data:
        return (jsonify({'error': 'Missing password'}), 400)

    MyUser = User(**data)
    storage.new(MyUser)
    storage.save()
    return (jsonify(MyUser.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def Update_user(user_id):
    """ Updates Object """
    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    MyVar = storage.all('User')
    obj = 'User' + '.' + user_id
    if obj in MyVar:
        for k, v in data.items():
            if k != 'id' or k != 'created_at' or k != 'updated_at':
                setattr(MyVar[obj], k, v)
        storage.save()
        return (jsonify(MyVar[obj].to_dict()), 200)
    else:
        return abort(404)
