#!/usr/bin/python3
""" States views """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def Retrieve_Cities(state_id):
    """ list cities"""
    MyState = storage.all()
    obj = 'State' + '.' + state_id
    MyCity = []
    if obj in MyState.keys():
        table_cities = MyState[obj].cities
        for city in table_cities:
                MyCity.append(city.to_dict())
        return jsonify(MyCity)
    else:
        return (abort(404))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def Retrieve_Cities2(city_id):
    """ list cities"""
    MyCity = storage.all('City')
    obj = 'City' + '.' + city_id
    """ if obj not in MyCity.keys(): """

    if obj in MyCity.keys():
        return jsonify(MyCity[obj].to_dict())
    return (abort(404))


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def Delete_obj(city_id):
    """Delete Obj"""
    data = storage.all('City')
    obj = 'City' + '.' + city_id
    if obj in data:
        storage.delete(data[obj])
        storage.save()
        return (jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def Create_obj(state_id):
    """ Create Obj """
    Id_state = storage.all('State')
    obj = 'State' + '.' + state_id

    if obj not in Id_state.keys():
        return abort(404)

    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in data:
        return (jsonify({'error': 'Missing name'}), 400)

    data['state_id'] = state_id
    MyCity = City(**data)
    storage.new(MyCity)
    storage.save()
    return (jsonify(MyCity.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def Update_obj(city_id):
    """ Update obj """
    MyVar = storage.all('City')
    obj = 'City' + '.' + city_id

    if obj not in MyVar.keys():
        return abort(404)

    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    for k, v in data.items():
        if k != 'id' or k != 'created_at' or k != 'updated_at':
            setattr(MyVar[obj], k, v)
        storage.save()
        return (jsonify(MyVar[obj].to_dict()), 200)
