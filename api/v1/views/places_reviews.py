#!/usr/bin/python3
""" Places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def Retrieve_Review(place_id):
    """ list Places"""
    MyPlace = storage.all()
    obj = 'Place' + '.' + place_id
    MyReview = []
    if obj in MyPlace.keys():
        table_review = MyPlace[obj].reviews
        for review in table_review:
                MyReview.append(review.to_dict())
        return jsonify(MyReview)
    else:
        return (abort(404))


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def Retrieve_Review2(review_id):
    """Shows Review"""
    MyReview = storage.all('Review')
    obj = 'Review' + '.' + review_id
    if obj in MyReview.keys():
        return jsonify(MyReview[obj].to_dict())
    return (abort(404))


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def Delete_Review(review_id):
    """Delete Review"""
    data = storage.all('Review')
    obj = 'Review' + '.' + review_id
    if obj in data.keys():
        storage.delete(data[obj])
        storage.save()
        return (jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def Create_Review(place_id):
    """ Creates Obj"""
    Id_place = storage.all('Place')
    obj = 'Place' + '.' + place_id
    if obj not in Id_place.keys():
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
    if 'text' not in data.keys():
        return (jsonify({'error': 'Missing text'}), 400)
    data['place_id'] = place_id
    MyReview = Review(**data)
    storage.new(MyReview)
    storage.save()
    return (jsonify(MyReview.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def Update_Reviews(review_id):
    """ Update review"""
    MyVar = storage.all('Review')
    obj = 'Review' + '.' + review_id
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
