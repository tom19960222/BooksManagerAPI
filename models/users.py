import time

from flask import jsonify

from models.utils.tokenutils import getTokenExpireTime, changeTokenUser

#!/usr/bin/python
# coding: UTF-8
from flask import abort, request
from bson.json_util import dumps

from models.database import usersdb
from models.logger import log
from utils.userutils import get_user_id_by_token
from views.JSONResponse.UserJSONResponse import *
from views.JSONResponse.TokenJSONResponse import *
from views.JSONResponse.LoginJSONResponse import *
from views.JSONResponse.CommonJSONResponse import *

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
        return JSONResponseUserNotFound
    if len(tmpusers) == 0:
        return JSONResponseUserNotFound
    return JSONResponse(dumps(tmpusers))

def add_user(username, password, email):
    if usersdb.find_one({'email': email}):
        return JSONResponseUserAlreadyExist
    tmpusers = usersdb.find().sort([('user_id', -1)]).limit(1)

    lastuser = None
    for user in tmpusers:
        lastuser = user
    new_user_id = 1
    if lastuser is not None and 'user_id' in lastuser:
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
    return JSONResponse(dumps(tmpuser))

def del_user(user_id):
    tmpuser = usersdb.find_one({'user_id': user_id})
    if tmpuser is None:
        abort(404)
    tmpuser = usersdb.update({'user_id': user_id}, {'$set': {'deactivated': True}})
    log("User %s deactivated" % user_id)
    return JSONResponse(dumps(tmpuser))

def update_user(user_id, username, password, email):
    tmpuser = usersdb.find_one({'user_id': user_id})
    jsondata = request.get_json()
    if tmpuser is None:
        return JSONResponseUserNotFound
    if not jsondata:
        return JSONResponseInvalidJSON

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

def login(email, password, token):
    log ("user %s is logging in, password = %s, token = %s" % (email, password, token))
    if time.time() > getTokenExpireTime(token):
        log("token %s expired" % (token))
        return JSONREsponseTokenExpired
    tmpuser = usersdb.find_one({'email': email})
    if tmpuser is None:
        log("User %s not found." % email)
        return JSONResponseUserNotFound
    if tmpuser['deactivated'] is True:
        return JSONResponseUserDeactivated
    if tmpuser['password'] == password:
        changeTokenUser(token, tmpuser['user_id'])
        log("User %s logged in with token %s" % (email, token))
        return JSONResponse(dumps(tmpuser))
    else:
        log(("User %s logged in with wrong password") % email)
        return JSONResponseWrongPassword

def logout(token):
    changeTokenUser(token, 0)
    log("user %s with token %s is logouted." % (get_user_id_by_token(token), token))
    return JSONResponseUserLogoutSuccessful
