#!/usr/bin/python
# coding: UTF-8
from flask import Blueprint, abort
from bson.json_util import dumps
from database import tokensdb
from logger import log
import string, random, time

tokenapi = Blueprint('tokenapi', __name__, url_prefix='/api/token')

access_tokens = [
    {
	'token' : 'fjrubrifgkdjnidjvisdjoj',
	'user_id' : 0,
	'expire_time' : 1429867579
    }
]

expire_seconds = 86400

def generateAccessToken():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))

@tokenapi.route('', methods=["GET"])
def get_token():
    randomToken = generateAccessToken()
    expire_time = int(time.time()) + expire_seconds
    tmptoken = {
        'token': randomToken,
        'user_id': 0,
        'expire_time': expire_time
    }
    tokensdb.insert_one(tmptoken)
    access_tokens.append(tmptoken)
    log("Token %s generated, expired when %s seconds" % (randomToken, expire_time))
    return dumps(tmptoken)

@tokenapi.route('/<token>', methods=["GET"])
def get_token_by_token(token):
    if token == "ALL":
        tmptoken = tokensdb.find()
    else:
        tmptoken = tokensdb.find_one({'token': token})
        if len(tmptoken) == 0:
            abort(404)
    return dumps(tmptoken)
