#!/usr/bin/python
#coding: UTF-8
from flask import Blueprint, request

from models.utils.userutils import get_user_id_by_token
from models.tokens import isErrorToken
from models.users import checkUserErrorByToken
from models.utils.commonutils import isfloat
from views.JSONResponse.CommonJSONResponse import *
from views.JSONResponse.BookJSONResponse import *
from views.templates.JSONResponse import makeResponse
import models.books


booksapi = Blueprint('booksapi', __name__, url_prefix='/api/book')

books = [
    {
        'book_id': 0,
        'bookname': u'雨港基隆 - 桐花雨',
        'author': u'東方紅',
        'publisher': u'尖端出版',
        'publish_date': '20150101',
        'price': 200,
        'ISBN': '1234567890',
        'user_id': 1
    }
]

@booksapi.route('', methods=['GET'])
def list_all_books():
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    response = models.books.list_all_books(get_user_id_by_token(token))
    return response.response_message, response.response_code

@booksapi.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    response = models.books.get_book_by_id(get_user_id_by_token(token), book_id)
    return response.response_message, response.response_code

@booksapi.route('', methods=['POST'])
def add_book():
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
    if 'bookname' not in jsondata:
        return makeResponse(JSONResponseProvideAtLeastBookName)

    bookname = ""
    author = ""
    publisher = ""
    publish_date = ""
    price = 0
    ISBN = ""
    tags = []
    cover_image_url = ""
    category_id = []

    if 'bookname' in jsondata:
        bookname = jsondata['bookname']
    if 'author' in jsondata:
        author = jsondata['author']
    if 'publisher' in jsondata:
        publisher = jsondata['publisher']
    if 'publish_date' in jsondata:
        publish_date = jsondata['publish_date']
    if 'price' in jsondata:
        price = jsondata['price']
    if 'ISBN' in jsondata:
        ISBN = jsondata['ISBN']
    if 'tags' in jsondata:
        tags = jsondata['tags']
    if 'cover_image_url' in jsondata:
        cover_image_url = jsondata['cover_image_url']
    if 'category_id' in jsondata:
        category_id = jsondata['category_id']

    if not isfloat(price):
        return makeResponse(JSONResponsePriceNotNumber)

    user_id = get_user_id_by_token(request.headers.get('Token'))

    response = models.books.add_book(user_id, bookname, author, publisher, publish_date, price, ISBN, tags, cover_image_url, category_id)
    return response.response_message, response.response_code


@booksapi.route('/<int:book_id>', methods=['DELETE'])
def del_book(book_id):
    token = request.headers.get('Token')
    ErrorResponse = isErrorToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    ErrorResponse = checkUserErrorByToken(token)
    if ErrorResponse is not None:
        return makeResponse(ErrorResponse)
    tmpuserid = get_user_id_by_token(token)
    response = models.books.del_book(tmpuserid, book_id)
    return response.response_message, response.response_code

@booksapi.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
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

    tmpuserid = get_user_id_by_token(token)
    bookname = ""
    author = ""
    publisher = ""
    publish_date = ""
    price = 0
    ISBN = ""
    tags = []
    cover_image_url = ""

    if 'bookname' in jsondata:
        bookname = jsondata['bookname']
    if 'author' in jsondata:
        author = jsondata['author']
    if 'publisher' in jsondata:
        publisher = jsondata['publisher']
    if 'publish_date' in jsondata:
        publish_date = jsondata['publish_date']
    if 'price' in jsondata:
        price = jsondata['price']
    if 'ISBN' in jsondata:
        ISBN = jsondata['ISBN']
    if 'tags' in jsondata:
        tags = jsondata['tags']
    if 'cover_image_url' in jsondata:
        cover_image_url = jsondata['cover_image_url']

    if not isfloat(price):
        return makeResponse(JSONResponsePriceNotNumber)

    response = models.books.update_book(tmpuserid, book_id, bookname, author, publisher, publish_date, price, ISBN, tags, cover_image_url)
    return response.response_message, response.response_code