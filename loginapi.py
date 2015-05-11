from flask import Blueprint, abort, request, jsonify
from pymongo import MongoClient
from tokenutils import get_token_expire_time, change_token_user
from database import usersdb
from logger import log
import time

loginapi = Blueprint('loginapi', __name__, url_prefix='/api/user/login')

@loginapi.route('', methods=['POST'])
def login():
    jsondata = request.get_json()
    if not jsondata:
        abort(400)
    username = jsondata['username']
    password = jsondata['password']
    token = request.headers.get('Token')
    print ("user %s is logging in, password = %s, token = %s" % (username, password, token))
    if username is None or password is None or token is None:
        abort(400)
    if time.time() > get_token_expire_time(token):
        log("token %s expired" % (token))
        return jsonify({'message': "Token expired"}), 403
    tmpuser = usersdb.find_one({'username': username})
    if tmpuser is None:
        print("User %s not found." % (username))
        return jsonify({'message': "User not found"}), 404
    if tmpuser['password'] == password:
        change_token_user(token, tmpuser['user_id'])
        log("User %s logged in with token %s"% (username, token))
        return jsonify({'message': "Login successful"})
    else:
        log("User %s logged in with wrong password")
        return jsonify({'message': "Wrong password."}), 403
