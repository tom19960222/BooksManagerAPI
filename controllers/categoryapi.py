#!/usr/bin/python
#coding: UTF-8
from flask import Blueprint, request

from models.utils.userutils import get_user_id_by_token
from models.tokens import isErrorToken
from models.users import checkUserErrorByToken
from views.JSONResponse.CommonJSONResponse import *
from views.JSONResponse.LoginJSONResponse import *
from views.templates.JSONResponse import makeResponse
import models.category


categoryapi = Blueprint('categoryapi', __name__, url_prefix='/api/category')


@categoryapi.route('', methods=['GET'])
def list_all_category():
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    response = models.category.list_all_category(get_user_id_by_token(token))
    return response.response_message, response.response_code

@categoryapi.route('/<int:category_id>', methods=['GET'])
def get_category_by_name(category_id):
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    response = models.category.get_category_by_id(get_user_id_by_token(token), category_id)
    return response.response_message, response.response_code

@categoryapi.route('', methods=['POST'])
def add_category():
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
    if 'category_name' not in jsondata:
        return makeResponse(JSONResponseProvideNecessaryInfo)

    category_name = jsondata['category_name']
    user_id = get_user_id_by_token(request.headers.get('Token'))

    response = models.category.add_category(user_id, category_name)
    return response.response_message, response.response_code


@categoryapi.route('/<int:category_id>', methods=['POST'])
def add_books_to_category(category_id):
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
    if 'books' not in jsondata:
        return makeResponse(JSONResponseProvideNecessaryInfo)

    user_id = get_user_id_by_token(request.headers.get('Token'))
    books = jsondata['books']
    response = models.category.add_books_to_category(user_id, category_id, books)
    return response.response_message, response.response_code


@categoryapi.route('', methods=['DELETE'])
def del_category():
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
    if 'category_id' not in jsondata:
        return makeResponse(JSONResponseProvideNecessaryInfo)
    category_id = jsondata['category_id']

    response = models.category.del_category(user_id, category_id)
    return response.response_message, response.response_code

@categoryapi.route('/<int:category_id>', methods=['DELETE'])
def del_book_from_category(category_id):
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
    if 'books' not in jsondata:
        return makeResponse(JSONResponseProvideNecessaryInfo)

    user_id = get_user_id_by_token(request.headers.get('Token'))
    books = jsondata['books']
    response = models.category.del_books_from_category(user_id, category_id, books)
    return response.response_message, response.response_code



@categoryapi.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
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
    if 'category_name' not in jsondata:
        makeResponse(JSONResponseProvideNecessaryInfo)
    category_name = jsondata['category_name']

    user_id = get_user_id_by_token(request.headers.get('Token'))

    response = models.category.update_category(user_id, category_id, category_name)
    return response.response_message, response.response_code