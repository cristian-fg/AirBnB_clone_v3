#!/usr/bin/python3
""" pets views """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.owner import Owner
from models.pet import Pet


@app_views.route('/owners/<owner_id>/pets', methods=['GET'],
                 strict_slashes=False)
def Retrieve_pets(owner_id):
    """ list pets"""
    Myowner = storage.all()
    obj = 'Owner' + '.' + owner_id
    Mypet = []
    if obj in Myowner.keys():
        table_owners = Myowner[obj].pets
        for pet in table_owners:
                Mypet.append(pet.to_dict())
        return jsonify(Mypet)
    else:
        return (abort(404))


@app_views.route('/pets/<pet_id>', methods=['GET'], strict_slashes=False)
def Retrieve_pet(pet_id):
    """ list pets"""
    Mypet = storage.all('Pet')
    obj = 'Pet' + '.' + pet_id

    if obj in Mypet.keys():
        return jsonify(Mypet[obj].to_dict())
    return (abort(404))


@app_views.route('/pets/<pet_id>', methods=['DELETE'],
                 strict_slashes=False)
def Delete_pet(pet_id):
    """Delete Obj"""
    data = storage.all('Pet')
    obj = 'Pet' + '.' + pet_id
    if obj in data:
        storage.delete(data[obj])
        storage.save()
        return (jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/owners/<owner_id>/pets', methods=['POST'],
                 strict_slashes=False)
def Create_pet(owner_id):
    """ Create Obj """
    Id_owner = storage.all('Owner')
    obj = 'Owner' + '.' + owner_id

    if obj not in Id_owner.keys():
        return abort(404)

    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in data:
        return (jsonify({'error': 'Missing name'}), 400)

    if 'age' not in data:
        return (jsonify({'error': 'Missing age'}), 400)

    if 'color' not in data:
        return (jsonify({'error': 'Missing color'}), 400)

    data['owner_id'] = owner_id
    Mypet = Pet(**data)
    storage.new(Mypet)
    storage.save()
    return (jsonify(Mypet.to_dict()), 201)


@app_views.route('/pets/<pet_id>', methods=['PUT'], strict_slashes=False)
def Update_pet(pet_id):
    """ Update obj """
    MyVar = storage.all('Pet')
    obj = 'Pet' + '.' + pet_id

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
