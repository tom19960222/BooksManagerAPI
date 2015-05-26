from flask import Blueprint, request
from views.templates.JSONResponse import makeResponse
from views.JSONResponse.CommonJSONResponse import *
from views.JSONResponse.LoginJSONResponse import *
import models.users


loginapi = Blueprint('loginapi', __name__, url_prefix='/api/user')

@loginapi.route('/login', methods=['POST'])
def login():
    jsondata = request.get_json()
    if not jsondata:
        return makeResponse(JSONResponseInvalidJSON)

    email = None
    password = None
    if 'email' in jsondata:
        email = jsondata['email']
    if 'password' in jsondata:
        password = jsondata['password']
    token = request.headers.get('Token')
    if email is None or password is None or token is None:
        return makeResponse(JSONResponseProvideNecessaryInfo)

    response = models.users.login(email, password, token)
    return response.response_message, response.response_code

@loginapi.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Token')
    if not token:
        return makeResponse(JSONResponseProvideNecessaryInfo)
    response = models.users.logout(token)
    return response.response_message, response.response_code

