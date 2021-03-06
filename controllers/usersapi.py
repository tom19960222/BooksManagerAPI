#!/usr/bin/python
# coding: UTF-8
from flask import Blueprint, request
from models.database import usersdb
from models.tokens import isErrorToken
from views.JSONResponse.CommonJSONResponse import *
from views.JSONResponse.UserJSONResponse import *
from views.JSONResponse.LoginJSONResponse import *
from views.templates.JSONResponse import makeResponse
import models.users

usersapi = Blueprint('userapi', __name__, url_prefix='/api/user')

@usersapi.route('', methods=['GET'])
def list_all_users():
    response = models.users.list_all_users()
    return response.response_message, response.response_code

@usersapi.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    response = models.users.get_user_by_id(user_id)
    return response.response_message, response.response_code

@usersapi.route('', methods=['POST'])
def add_user():
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)

    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    jsondata = request.get_json()
    if not jsondata:
        return makeResponse(JSONResponseInvalidJSON)
    if 'username' not in jsondata or 'password' not in jsondata or 'email' not in jsondata:
        return makeResponse(JSONResponseProvideNecessaryInfo)
    username = jsondata['username']
    password = jsondata['password']
    email = jsondata['email']
    head_image_url = ""
    if 'head_image_url' in jsondata:
        head_image_url = jsondata['head_image_url']
    response = models.users.add_user(username, password, email, head_image_url, token)
    return response.response_message, response.response_code

@usersapi.route('/<int:user_id>', methods=['DELETE'])
def del_user(user_id):
    response = models.users.del_user(user_id)
    return response.response_message, response.response_code

@usersapi.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    tmpuser = usersdb.find_one({'user_id': user_id})
    jsondata = request.get_json()
    if tmpuser is None:
        return makeResponse(JSONResponseUserNotFound)
    if not jsondata:
        return makeResponse(JSONResponseInvalidJSON)

    username = ""
    password = ""
    head_image_url = ""

    if 'username' in jsondata:
        username = jsondata['username']
    if 'password' in jsondata:
        password = jsondata['password']
    if 'head_image_url' in jsondata:
        head_image_url = jsondata['head_image_url']
    response = models.users.update_user(user_id, username, password, head_image_url)
    return response.response_message, response.response_code