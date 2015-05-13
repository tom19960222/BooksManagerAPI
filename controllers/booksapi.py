#!/usr/bin/python
#coding: UTF-8
from flask import Blueprint, request
from flask import jsonify

from models.utils.userutils import get_user_id_by_token, checkIsVaildUserWithToken
from views.templates.jsonresponse import JSONResponse
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
    reqtoken = request.headers.get('Token')
    if not checkIsVaildUserWithToken(reqtoken):
        return JSONResponse(jsonify({'message': 'Please log in first.'}), 401)
    response = models.books.list_all_books(get_user_id_by_token(reqtoken))
    return response.response_message, response.response_code

@booksapi.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    reqtoken = request.headers.get('Token')
    if not checkIsVaildUserWithToken(reqtoken):
        return JSONResponse(jsonify({'message': 'Please log in first.'}), 401)
    response = models.books.get_book_by_id(get_user_id_by_token(reqtoken), book_id)
    return response.response_message, response.response_code

@booksapi.route('', methods=['POST'])
def add_book():
    token = request.headers.get('Token')
    if not token:
        return JSONResponse(jsonify({'message': 'Please provide token.'}), 401)
    if not checkIsVaildUserWithToken(token):
        return JSONResponse(jsonify({'message': 'Please login first.'}), 403) # User not login is not allow to add books.
    jsondata = request.get_json()
    if not jsondata:
        return JSONResponse(jsonify({'message': 'Invaild JSON request.'}), 400)
    if 'bookname' not in jsondata:
        return JSONResponse(jsonify({'message': 'Please provide at least book name.'}), 400)

    bookname = ""
    author = ""
    publisher = ""
    publish_date = ""
    price = ""
    ISBN = ""

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
    user_id = get_user_id_by_token(request.headers.get('Token'))

    response = models.books.add_book(user_id, bookname, author, publisher, publish_date, price, ISBN)
    return response.response_message, response.response_code


@booksapi.route('/<int:book_id>', methods=['DELETE'])
def del_book(book_id):
    token = request.headers.get('Token')
    if not token:
        return JSONResponse(jsonify({'message': 'Please provide token.'}), 401)
    if get_user_id_by_token(request.headers.get('Token')) == 0:
        return JSONResponse(jsonify({'message': 'Please login first.'}), 403) # User not login is not allow to delete books.
    tmpuserid = get_user_id_by_token(token)
    response = models.books.del_book(tmpuserid, book_id)
    return response.response_message, response.response_code

@booksapi.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    tmpuserid = get_user_id_by_token(request.headers.get('Token'))
    jsondata = request.get_json()
    if not jsondata:
        return JSONResponse(jsonify({'message': 'Invaild JSON request.'}), 400)

    bookname = ""
    author = ""
    publisher = ""
    publish_date = ""
    price = ""
    ISBN = ""

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

    response = models.books.update_book(tmpuserid, book_id, bookname, author, publisher, publish_date, price, ISBN)
    return response.response_message, response.response_code