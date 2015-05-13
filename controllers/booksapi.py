#!/usr/bin/python
#coding: UTF-8
from flask import Blueprint, jsonify, abort, request
from bson.json_util import dumps
from models.utils.userutils import get_user_id_by_token
from models.database import booksdb
from models.logger import log


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
    tmpuserid = get_user_id_by_token(reqtoken)
    if tmpuserid == 0:
        abort(401)
    tmpbooks = booksdb.find({'$and': [{'user_id': tmpuserid}, {'deleted': False}]})
    return dumps(tmpbooks)

@booksapi.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    reqtoken = request.headers.get('Token')
    tmpuserid = get_user_id_by_token(reqtoken)
    if tmpuserid == 0:
        abort(401)
    tmpbooks = booksdb.find({'$and': [{'user_id': tmpuserid}, {'book_id': book_id}]})
    return dumps(tmpbooks)

@booksapi.route('', methods=['POST'])
def add_book():
    if not request.headers.get('Token'):
        abort(400)
    if get_user_id_by_token(request.headers.get('Token')) == 0:
        abort(403) # User not login is not allow to add books.

    jsondata = request.get_json()

    if not jsondata:
        abort(400)
    if 'bookname' not in jsondata:
        abort(400)

    new_book_id = 1
    tmpbooks = booksdb.find().sort([('book_id', -1)]).limit(1)
    for book in tmpbooks:
        lastbook = book
    if lastbook['user_id'] is not None:
        new_book_id = int(lastbook['book_id'])+1

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

    tmpbook = {
        'book_id' : new_book_id,
        'bookname' : bookname,
        'author': author,
        'publisher': publisher,
        'publish_date': publish_date,
        'price': price,
        'ISBN': ISBN,
        'user_id': user_id,
        'deleted': False
    }

    booksdb.insert(tmpbook)
    print("User %s created a book, id=%s, bookname=\"%s\", author=\"%s\", publisher=\"%s\", publish_date=\"%s\", price=\"%s\", ISBN=\"%s\"" \
          % (user_id, new_book_id, bookname, author, publisher, publish_date, price, ISBN))
    return dumps(tmpbook), 201

@booksapi.route('/<int:book_id>', methods=['DELETE'])
def del_book(book_id):
    if not request.headers.get('Token'):
        abort(400)
    if get_user_id_by_token(request.headers.get('Token')) == 0:
        abort(403) # User not login is not allow to delete books.
    tmpuserid = get_user_id_by_token(request.headers.get('Token'))
    tmpbook = booksdb.find_one({'$and': [{'user_id': tmpuserid}, {'book_id': book_id}]})
    if len(tmpbook) == 0:
        abort(404)
    booksdb.update({'$and': [{'user_id': tmpuserid}, {'book_id': book_id}]}, {'$set': {'deleted': True}})
    print("User %s deleted book %s" % (tmpuserid, book_id))
    return jsonify({'message': 'Book %s deleted successful.' % (book_id)})

@booksapi.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    tmpuserid = get_user_id_by_token(request.headers.get('Token'))
    tmpbook = booksdb.find_one({'$and': [{'user_id': tmpuserid}, {'book_id': book_id}]})
    jsondata = request.get_json()
    if len(tmpbook) == 0:
        abort(404)
    if not jsondata:
        abort(400)

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

    if bookname != "":
        booksdb.update({'user_id': tmpuserid}, {'$set': {'bookname': bookname}})
        log("Updated user %s's book %s's bookname to %s" % (tmpuserid, book_id, bookname))
    if author != "":
        booksdb.update({'user_id': tmpuserid}, {'$set': {'author': author}})
        log("Updated user %s's book %s's author to %s" % (tmpuserid, book_id, author))
    if publisher != "":
        booksdb.update({'user_id': tmpuserid}, {'$set': {'publisher': publisher}})
        log("Updated user %s's book %s's publisher to %s" % (tmpuserid, book_id, publisher))
    if publish_date != "":
        booksdb.update({'user_id': tmpuserid}, {'$set': {'publish_date': publish_date}})
        log("Updated user %s's book %s's publish_date to %s" % (tmpuserid, book_id, publish_date))
    if price != "":
        booksdb.update({'user_id': tmpuserid}, {'$set': {'price': price}})
        log("Updated user %s's book %s's price to %s" % (tmpuserid, book_id, price))
    if ISBN != "":
        booksdb.update({'user_id': tmpuserid}, {'$set': {'ISBN': ISBN}})
        log("Updated user %s's book %s's ISBN to %s" % (tmpuserid, book_id, ISBN))

    tmpbook = booksdb.find_one({'$and': [{'user_id': tmpuserid}, {'book_id': book_id}]})
    return dumps(tmpbook)