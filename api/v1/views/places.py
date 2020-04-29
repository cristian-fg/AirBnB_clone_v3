#!/usr/bin/python3
""" Places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def Retrieve_Places(city_id):
    """ list Places"""
    MyCity = storage.all()
    obj = 'City' + '.' + city_id
    MyPlace = []
    if obj in MyCity.keys():
        table_place = MyCity[obj].places
        for place in table_place:
                MyPlace.append(place.to_dict())
        return jsonify(MyPlace)
    else:
        return (abort(404))


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def Retrieve_Places2(place_id):
    """list Places"""
    MyPlace = storage.all('Place')
    obj = 'Place' + '.' + place_id
    if obj in MyPlace.keys():
        return jsonify(MyPlace[obj].to_dict())
    return (abort(404))


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def Delete_place(place_id):
    """Deletes Place"""
    data = storage.all('Place')
    obj = 'Place' + '.' + place_id
    if obj in data.keys():
        storage.delete(data[obj])
        storage.save()
        return (jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def Create_ob(city_id):
    """Creates Obj"""
    Id_city = storage.all('City')
    obj = 'City' + '.' + city_id
    if obj not in Id_city.keys():
        return abort(404)
    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in data.keys():
        return (jsonify({'error': 'Missing user_id'}), 400)
    MyUser = storage.all('User')
    Data2 = data['user_id']
    if "User." + Data2 not in MyUser.keys():
        return (abort(404))
    if 'name' not in data.keys():
        return (jsonify({'error': 'Missing name'}), 400)
    data['city_id'] = city_id
    MyPlace = Place(**data)
    storage.new(MyPlace)
    storage.save()
    return (jsonify(MyPlace.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def Update_ob(place_id):
    """Update"""
    MyVar = storage.all('Place')
    obj = 'Place' + '.' + place_id
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
