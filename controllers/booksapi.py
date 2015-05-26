#!/usr/bin/python
#coding: UTF-8
from flask import Blueprint, request

from models.utils.userutils import get_user_id_by_token, checkIsVaildUserWithToken
from models.utils.tokenutils import isTokenExpired
from views.JSONResponse.CommonJSONResponse import *
from views.JSONResponse.BookJSONResponse import *
from views.JSONResponse.TokenJSONResponse import *
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
    if not token:
        return makeResponse(JSONResponseProvideToken)
    if not checkIsVaildUserWithToken(token):
        return makeResponse(JSONResponseLoginFirst)
    if isTokenExpired(token):
        return makeResponse(JSONREsponseTokenExpired)
    response = models.books.list_all_books(get_user_id_by_token(token))
    return response.response_message, response.response_code

@booksapi.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    token = request.headers.get('Token')
    if not token:
        return makeResponse(JSONResponseProvideToken)
    if not checkIsVaildUserWithToken(token):
        return makeResponse(JSONResponseLoginFirst)
    if isTokenExpired(token):
        return makeResponse(JSONREsponseTokenExpired)
    response = models.books.get_book_by_id(get_user_id_by_token(token), book_id)
    return response.response_message, response.response_code

@booksapi.route('', methods=['POST'])
def add_book():
    token = request.headers.get('Token')
    if not token:
        return makeResponse(JSONResponseProvideToken)
    if not checkIsVaildUserWithToken(token):
        return makeResponse(JSONResponseLoginFirst)
    if isTokenExpired(token):
        return makeResponse(JSONREsponseTokenExpired)
    jsondata = request.get_json()
    if not jsondata:
        return makeResponse(JSONResponseInvalidJSON)
    if 'bookname' not in jsondata:
        return makeResponse(JSONResponseProvideAtLeastBookName)
    bookname = ""
    author = ""
    publisher = ""
    publish_date = ""
    price = ""
    ISBN = ""
    tags = []

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
    user_id = get_user_id_by_token(request.headers.get('Token'))

    response = models.books.add_book(user_id, bookname, author, publisher, publish_date, price, ISBN, tags)
    return response.response_message, response.response_code


@booksapi.route('/<int:book_id>', methods=['DELETE'])
def del_book(book_id):
    token = request.headers.get('Token')
    if not token:
        return makeResponse(JSONResponseProvideToken)
    if not checkIsVaildUserWithToken(token):
        return makeResponse(JSONResponseLoginFirst) # User not login is not allow to delete books.
    if isTokenExpired(token):
        return makeResponse(JSONREsponseTokenExpired)
    tmpuserid = get_user_id_by_token(token)
    response = models.books.del_book(tmpuserid, book_id)
    return response.response_message, response.response_code

@booksapi.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    token = request.headers.get('Token')
    tmpuserid = get_user_id_by_token(token)
    jsondata = request.get_json()
    if not token:
        return makeResponse(JSONResponseProvideToken)
    if not jsondata:
        return makeResponse(JSONResponseInvalidJSON)
    if isTokenExpired(token):
        return makeResponse(JSONREsponseTokenExpired)

    bookname = ""
    author = ""
    publisher = ""
    publish_date = ""
    price = ""
    ISBN = ""
    tags = []

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

    response = models.books.update_book(tmpuserid, book_id, bookname, author, publisher, publish_date, price, ISBN, tags)
    return response.response_message, response.response_code