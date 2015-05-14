from flask import Blueprint, abort, request

from views.JSONResponse.CommonJSONResponse import *
from views.JSONResponse.LoginJSONResponse import *
import models.users


loginapi = Blueprint('loginapi', __name__, url_prefix='/api/user/login')

@loginapi.route('', methods=['POST'])
def login():
    jsondata = request.get_json()
    if not jsondata:
        return JSONResponseInvalidJSON
    username = jsondata['username']
    password = jsondata['password']
    token = request.headers.get('Token')
    if username is None or password is None or token is None:
        return JSONResponseProvideNecessaryInfo

    response = models.users.login(username, password, token)
    return response.response_message, response.response_code
