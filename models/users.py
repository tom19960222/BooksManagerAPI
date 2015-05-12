import time

from flask import Blueprint, abort, request, jsonify

from models.utils.tokenutils import get_token_expire_time, change_token_user

#!/usr/bin/python
# coding: UTF-8
from flask import Blueprint, abort, request
from bson.json_util import dumps

from models.database import usersdb
from models.logger import log
from views.jsonresponse import JSONResponse

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

def list_all_users():
    return JSONResponse(dumps(usersdb.find({'deactivated': False})))

def get_user_by_id(user_id):
    tmpusers = usersdb.find_one({'user_id': user_id})
    if tmpusers is None:
        abort(404)
    if len(tmpusers) == 0:
        abort(404)
    return JSONResponse(response_dict_or_string=dumps(tmpusers))

def add_user(username, password, email):
    tmpusers = usersdb.find().sort([('user_id', -1)]).limit(1)
    for user in tmpusers:
        lastuser = user
    new_user_id = 1
    if lastuser['user_id'] is not None:
        new_user_id = int(lastuser['user_id'])+1

    tmpuser = {
        'user_id': new_user_id,
        'username': username,
        'email': email,
        'password': password,
        'deactivated': False
    }

    usersdb.insert(tmpuser)
    log("User %s created, username = %s, password = %s, email = %s" % (new_user_id, username, password, email))
    return JSONResponse(response_dict_or_string=dumps(tmpuser))

def del_user(user_id):
    tmpuser = usersdb.find_one({'user_id': user_id})
    if tmpuser is None:
        abort(404)
    tmpuser = usersdb.update({'user_id': user_id}, {'$set': {'deactivated': True}})
    log("User %s deactivated" % user_id)
    return JSONResponse(response_dict_or_string=dumps(tmpuser))

def update_user(user_id, username, password, email):
    tmpuser = usersdb.find_one({'user_id': user_id})
    jsondata = request.get_json()
    if tmpuser is None:
        abort(404)
    if not jsondata:
        abort(400)

    if type(jsondata['username']) is unicode:
        usersdb.update({'user_id': user_id}, {'$set': {'username': username}})
        log("Updated user %s's username to %s" % (user_id, username))
    if type(jsondata['email']) is unicode:
        usersdb.update({'user_id': user_id}, {'$set': {'email': email}})
        log("Updated user %s's email to %s" % (user_id, email))
    if type(jsondata['password']) is unicode:
        usersdb.update({'user_id': user_id}, {'$set': {'password': password}})
        log("Updated user %s's password to %s" % (user_id, password))

    tmpuser = usersdb.find_one({'user_id': user_id}) #Get updated data.
    return JSONResponse(dumps(tmpuser))

def login(username, password, token):
    print ("user %s is logging in, password = %s, token = %s" % (username, password, token))
    if time.time() > get_token_expire_time(token):
        log("token %s expired" % (token))
        return JSONResponse(jsonify({'message': "Token expired"}), 403)
    tmpuser = usersdb.find_one({'username': username})
    if tmpuser is None:
        print("User %s not found." % (username))
        return JSONResponse(jsonify({'message': "User not found"}), 404)
    if tmpuser['password'] == password:
        change_token_user(token, tmpuser['user_id'])
        log("User %s logged in with token %s"% (username, token))
        return JSONResponse(jsonify({'message': "Login successful"}))
    else:
        log("User %s logged in with wrong password")
        return JSONResponse(jsonify({'message': "Wrong password."}), 403)
