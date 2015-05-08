#!/usr/bin/python
# coding: UTF-8
from flask import Blueprint, jsonify, abort, request
from pymongo import MongoClient
from bson.json_util import dumps
import tokenapi
import time

usersapi = Blueprint('userapi', __name__, url_prefix='/api/user')
dbClient = MongoClient('163.13.128.116', 27017)
db = dbClient.BooksManagerTest1
usersdb = db.users
tokensdb = db.tokens

users = [
    {
        'user_id': 0,
        'username': 'Anonymous',
        'email': '',
        'password': '',
        'lastlogintime': '2015/04/08 15:59',
        'lastloginip': '127.0.0.1',
        'deactivated': True
    }
]

@usersapi.route('', methods=['GET'])
def list_all_users():
    return dumps(usersdb.find({'deactivated': False}))


@usersapi.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    tmpusers = usersdb.find_one({'user_id': user_id})
    if len(tmpusers) == 0:
        abort(404)
    return dumps(tmpusers)


@usersapi.route('', methods=['POST'])
def add_user():
    jsondata = request.get_json()
    if not jsondata or not 'username' in jsondata:
        abort(400)

    tmpusers = usersdb.find().sort([('user_id', -1)]).limit(1)
    for user in tmpusers:
        lastuser = user
    new_user_id = 1
    if lastuser['user_id'] is not None:
        new_user_id = int(lastuser['user_id'])+1

    tmpuser = {
        'user_id': new_user_id,
        'username': jsondata['username'],
        'email': jsondata['email'],
        'password': jsondata['password'],
        'deactivated': False
    }
    usersdb.insert(tmpuser)
    return dumps(tmpuser), 201


@usersapi.route('/<int:user_id>', methods=['DELETE'])
def del_user(user_id):
    tmpuser = usersdb.find_one({'user_id': user_id})
    if tmpuser is None:
        abort(404)

    tmpuser = usersdb.update({'user_id': user_id}, {'$set': {'deactivated': True}})
    return dumps(tmpuser)


@usersapi.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    tmpuser = usersdb.find_one({'user_id': user_id})
    jsondata = request.get_json()
    if tmpuser is None:
        abort(404)
    if not jsondata:
        abort(400)

    if 'username' in jsondata and type(jsondata['username']) is unicode:
        usersdb.update({'user_id': user_id}, {'$set': {'username': jsondata['username']}})
    if 'email' in jsondata and type(jsondata['email']) is unicode:
        usersdb.update({'user_id': user_id}, {'$set': {'email': jsondata['email']}})
    if 'password' in jsondata and type(jsondata['password']) is unicode:
        usersdb.update({'user_id': user_id}, {'$set': {'password': jsondata['password']}})

    tmpuser = usersdb.find_one({'user_id': user_id}) #Get updated data.
    return dumps(tmpuser)

@usersapi.route('/login', methods=['POST'])
def login():
    jsondata = request.get_json()
    if not jsondata:
        abort(400)
    username = jsondata['username']
    password = jsondata['password']
    token = request.headers.get('Token')
    if username is None or password is None or token is None:
        abort(400)
    if time.time() > tokenapi.get_token_expire_time(token):
        abort(403), "Token expired."
    tmpuser = usersdb.find_one({'username': username})
    if tmpuser is None: #Can't find the user.
        abort(404)
    if tmpuser['password'] == password:
        tokenapi.change_token_user(token, tmpuser['user_id'])
        return jsonify({'message': "Login successful"})
    else:
        return jsonify({'message': "Login failed"})


#@usersapi.route('/with_token/<token>', methods=['GET'])
def get_user_id_by_token(token):
    tmptoken = tokensdb.find_one({'token': token})
    return tmptoken['user_id']
#    return jsonify({"user_id": tmptoken['user_id']})
