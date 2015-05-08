#!/usr/bin/python
#coding: UTF-8
from flask import Blueprint, jsonify, abort, request
from pymongo import MongoClient
from bson.json_util import dumps
import usersapi

booksapi = Blueprint('booksapi', __name__, url_prefix='/api/book')
dbClient = MongoClient('163.13.128.116', 27017)
db = dbClient.BooksManagerTest1
booksdb = db.books

books = [
    {
        'book_id' : 0,
        'bookname' : u'雨港基隆 - 桐花雨',
        'author' : u'東方紅',
        'publisher' : u'尖端出版',
        'publish_date' : '20150101',
        'price' : 200,
        'ISBN' : '1234567890',
        'owned_user': [1,2]
    }
]

@booksapi.route('', methods=['GET'])
def list_all_books():
    reqtoken = request.headers.get('Token')
    tmpuserid = usersapi.get_user_id_by_token(reqtoken)
    tmpbooks = booksdb.find({'owned_user': {'$in': [tmpuserid]}})
    return dumps(tmpbooks)

@booksapi.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    #tmpbooks = [tmpbook for tmpbook in books if tmpbook['book_id'] == book_id]
    reqtoken = request.headers.get('Token')
    tmpuserid = usersapi.get_user_id_by_token(reqtoken)
    tmpbooks = booksdb.find({'$and': [{'owned_user': {'$in': [tmpuserid]}}, {'book_id': book_id}]})
    return dumps(tmpbooks)

@booksapi.route('', methods=['POST'])
def add_book():
    if not request.json or not 'bookname' in request.json:
        abort(400)
    tmpbooks = booksdb.find().sort([('book_id', -1)]).limit(1)
    for book in tmpbooks:
        lastbook = book
    new_user_id = 1
    if lastbook['user_id'] is not None:
        new_user_id = int(lastbook['book_id'])+1

    tmpbook = {
        'book_id' : books[-1]['book_id']+1,
        'bookname' : request.json['bookname']
    }
    books.append(tmpbook)
    return jsonify({'book':tmpbook}), 201

@booksapi.route('/<int:book_id>', methods=['DELETE'])
def del_book(book_id):
    tmpbook = [tmpbook for tmpbook in books if tmpbook['book_id'] == book_id]
    if len(tmpbook) == 0:
        abort(404)
    books.remove(tmpbook[0])
    return jsonify({'result':True})

@booksapi.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    tmpbook = [tmpbook for tmpbook in books if tmpbook['book_id'] == book_id]
    jsondata = request.get_json()
    if len(tmpbook) == 0:
        abort(404)
    if not jsondata:
        abort(400)

    if 'bookname' in request.json and type(request.json['bookname']) is unicode:
        tmpbook[0]['bookname'] = jsondata['bookname']
    if 'author' in request.json and type(request.json['author']) is unicode:
        tmpbook[0]['author'] = jsondata['author']
    if 'publisher' in request.json and type(request.json['publisher']) is unicode:
        tmpbook[0]['publisher'] = jsondata['publisher']
    if 'publish_date' in request.json and type(request.json['publish_date']) is unicode:
        tmpbook[0]['publish_date'] = jsondata['publish_date']
    if jsondata.get('price') is not None and type(jsondata['price']) is int:
        books[0]['price'] = jsondata['price']
        return jsonify({'book': tmpbook[0]})