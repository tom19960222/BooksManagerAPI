import time

from flask import Blueprint, abort, request, jsonify

import models.users

loginapi = Blueprint('loginapi', __name__, url_prefix='/api/user/login')

@loginapi.route('', methods=['POST'])
def login():
    jsondata = request.get_json()
    if not jsondata:
        abort(400)
    username = jsondata['username']
    password = jsondata['password']
    token = request.headers.get('Token')
    if username is None or password is None or token is None:
        abort(400)

    response = models.users.login(username, password, token)
    return response.response_message, response.response_code
