#!/usr/bin/python
#coding: UTF-8
from flask import Blueprint, request

from models.utils.userutils import get_user_id_by_token
from models.tokens import isErrorToken
from models.users import checkUserErrorByToken
from views.JSONResponse.CommonJSONResponse import *
from views.JSONResponse.LoginJSONResponse import *
from views.templates.JSONResponse import makeResponse
import models.catagory


catagoryapi = Blueprint('catagoryapi', __name__, url_prefix='/api/catagory')


@catagoryapi.route('', methods=['GET'])
def list_all_catagory():
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    response = models.catagory.list_all_catagory(get_user_id_by_token(token))
    return response.response_message, response.response_code

@catagoryapi.route('/<int:catagory_id>', methods=['GET'])
def get_catagory_by_name(catagory_id):
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    response = models.catagory.get_catagory_by_id(get_user_id_by_token(token), catagory_id)
    return response.response_message, response.response_code

@catagoryapi.route('', methods=['POST'])
def add_catagory():
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    jsondata = request.get_json()
    if not jsondata:
        return makeResponse(JSONResponseInvalidJSON)
    if 'catagory_name' not in jsondata:
        return makeResponse(JSONResponseProvideNecessaryInfo)

    catagory_name = jsondata['catagory_name']

    user_id = get_user_id_by_token(request.headers.get('Token'))

    response = models.catagory.add_catagory(user_id, catagory_name)
    return response.response_message, response.response_code


@catagoryapi.route('/<int:catagory_id>', methods=['POST'])
def add_books_to_catagory(catagory_id):
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    jsondata = request.get_json()
    if not jsondata:
        return makeResponse(JSONResponseInvalidJSON)
    if 'book_list' not in jsondata and 'book' not in jsondata:
        return makeResponse(JSONResponseProvideNecessaryInfo)

    user_id = get_user_id_by_token(request.headers.get('Token'))
    book_list = list()
    book = 1

    if 'book_list' in jsondata:
        book_list = jsondata['book_list']
    elif 'book' in jsondata:
        book = jsondata['book']

    if len(book_list) != 0:
        response = models.catagory.add_books_to_catagory(user_id, catagory_id, book_list)
    else:
        response = models.catagory.add_books_to_catagory(user_id, catagory_id, book)
    return response.response_message, response.response_code


@catagoryapi.route('', methods=['DELETE'])
def del_catagory():
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)

    user_id = get_user_id_by_token(request.headers.get('Token'))
    jsondata = request.get_json()
    if not jsondata:
        return makeResponse(JSONResponseInvalidJSON)
    if 'catagory_id' not in jsondata:
        return makeResponse(JSONResponseProvideNecessaryInfo)
    catagory_id = jsondata['catagory_id']

    response = models.catagory.del_catagory(user_id, catagory_id)
    return response.response_message, response.response_code

@catagoryapi.route('/<int:catagory_id>', methods=['DELETE'])
def del_book_from_catagory(catagory_id):
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)

    jsondata = request.get_json()
    if not jsondata:
        return makeResponse(JSONResponseInvalidJSON)
    if 'book_list' not in jsondata and 'book' not in jsondata:
        return makeResponse(JSONResponseProvideNecessaryInfo)

    book_list = list()
    book = ""
    user_id = get_user_id_by_token(request.headers.get('Token'))
    response = ""
    if 'book_list' in jsondata:
        book_list = jsondata['book_list']
        response = models.catagory.del_books_from_catagory(user_id, catagory_id, book_list)
    elif 'book' in jsondata:
        book = jsondata['book']
        response = models.catagory.del_books_from_catagory(user_id, catagory_id, book)

    return response.response_message, response.response_code



@catagoryapi.route('/<int:catagory_id>', methods=['PUT'])
def update_catagory(catagory_id):
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    jsondata = request.get_json()
    if not jsondata:
        return makeResponse(JSONResponseInvalidJSON)
    if 'catagory_name' not in jsondata:
        makeResponse(JSONResponseProvideNecessaryInfo)
    catagory_name = jsondata['catagory_name']
    user_id = get_user_id_by_token(request.headers.get('Token'))

    response = models.catagory.update_catagory(user_id, catagory_id, catagory_name)
    return response.response_message, response.response_code