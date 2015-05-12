#!/usr/bin/python
# coding: UTF-8
from flask import Blueprint, abort, request
from bson.json_util import dumps

from models.database import usersdb
from models.logger import log


usersapi = Blueprint('userapi', __name__, url_prefix='/api/user')

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
    if tmpusers is None:
        abort(404)
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

    username = jsondata['username']
    password = jsondata['password']
    email = jsondata['email']

    tmpuser = {
        'user_id': new_user_id,
        'username': jsondata['username'],
        'email': jsondata['email'],
        'password': jsondata['password'],
        'deactivated': False
    }
    usersdb.insert(tmpuser)
    log("User %s created, username = %s, password = %s, email = %s" % (new_user_id, username, password, email))
    return dumps(tmpuser), 201


@usersapi.route('/<int:user_id>', methods=['DELETE'])
def del_user(user_id):
    tmpuser = usersdb.find_one({'user_id': user_id})
    if tmpuser is None:
        abort(404)
    tmpuser = usersdb.update({'user_id': user_id}, {'$set': {'deactivated': True}})
    log("User %s deactivated" % user_id)
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
        log("Updated user %s's username to %s" % (user_id, jsondata['username']))
    if 'email' in jsondata and type(jsondata['email']) is unicode:
        usersdb.update({'user_id': user_id}, {'$set': {'email': jsondata['email']}})
        log("Updated user %s's email to %s" % (user_id, jsondata['email']))
    if 'password' in jsondata and type(jsondata['password']) is unicode:
        usersdb.update({'user_id': user_id}, {'$set': {'password': jsondata['password']}})
        log("Updated user %s's password to %s" % (user_id, jsondata['password']))

    tmpuser = usersdb.find_one({'user_id': user_id}) #Get updated data.
    return dumps(tmpuser)