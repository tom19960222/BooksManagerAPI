#!/usr/bin/python
# coding: UTF-8
from flask import Blueprint, jsonify, abort, request

usersapi = Blueprint('userapi', __name__, url_prefix='/api/user')

users = [
    {
        'user_id': 0,
        'username': 'Anonymous',
        'email': '',
        'password': '',
        'lastlogintime': '2015/04/08 15:59',
        'lastloginip': '127.0.0.1'
    }
]

@usersapi.route('', methods=['GET'])
def list_all_users():
    return jsonify({'users': users})


@usersapi.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    tmpusers = [tmpuser for tmpuser in users if tmpuser['user_id'] == user_id]

    if len(tmpusers) == 0:
        abort(404)
    return jsonify({'users': tmpusers[0]})


@usersapi.route('', methods=['POST'])
def add_user():
    jsondata = request.get_json()
    if not jsondata or not 'username' in jsondata:
        abort(400)
    tmpuser = {
        'user_id': users[-1]['user_id'] + 1,
        'username': jsondata['username'],
        'email': jsondata['email'],
        'password': jsondata['password']
    }
    users.append(tmpuser)
    return jsonify({'user': tmpuser}), 201


@usersapi.route('/<int:user_id>', methods=['DELETE'])
def del_user(user_id):
    tmpuser = [tmpuser for tmpuser in users if tmpuser['user_id'] == user_id]
    if len(tmpuser) == 0:
        abort(404)
    users.remove(tmpuser[0])
    return jsonify({'result': True})


@usersapi.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    tmpuser = [tmpuser for tmpuser in users if tmpuser['user_id'] == user_id]
    jsondata = request.get_json()
    if len(tmpuser) == 0:
        abort(404)
    if not jsondata:
        abort(400)

    if 'username' in request.json and type(request.json['username']) is unicode:
        tmpuser[0]['username'] = jsondata['username']
    if 'email' in request.json and type(request.json['email']) is unicode:
        tmpuser[0]['email'] = jsondata['email']
    if 'password' in request.json and type(request.json['password']) is unicode:
        tmpuser[0]['password'] = jsondata['password']
        return jsonify({'book': tmpuser[0]})
