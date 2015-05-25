from flask import Blueprint, abort, request
from views.templates.JSONRespons import makeResponse
from views.JSONResponse.CommonJSONResponse import *
from views.JSONResponse.LoginJSONResponse import *
import models.users


loginapi = Blueprint('loginapi', __name__, url_prefix='/api/user')

@loginapi.route('/login', methods=['POST'])
def login():
    jsondata = request.get_json()
    if not jsondata:
        return makeResponse(JSONResponseInvalidJSON)
    username = jsondata['username']
    password = jsondata['password']
    token = request.headers.get('Token')
    if username is None or password is None or token is None:
        return makeResponse(JSONResponseProvideNecessaryInfo)

    response = models.users.login(username, password, token)
    return response.response_message, response.response_code

@loginapi.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Token')
    if not token:
        return makeResponse(JSONResponseProvideNecessaryInfo)
    response = models.users.logout(token)
    return response.response_message, response.response_code

