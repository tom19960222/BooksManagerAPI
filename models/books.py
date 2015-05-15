#!/usr/bin/python
#coding: UTF-8
from flask import jsonify
from bson.json_util import dumps

from models.logger import log
from database import booksdb
from views.templates.JSONResponse import JSONResponse, makeResponse
from utils.bookutils import isBookExist


books = [
    {
        'book_id': 0,
        'bookname': u'雨港基隆 - 桐花雨',
        'author': u'東方紅',
        'publisher': u'尖端出版',
        'publish_date': '20150101',
        'price': 200,
        'ISBN': '1234567890',
        'tags': ['QQ', 'QQQ'],
        'cover_images_url': 'http://i.imgur.com/zNPKpwk.jpg',
        'user_id': 1
    }
]

def list_all_books(user_id):
    tmpbooks = booksdb.find({'$and': [{'user_id': user_id}, {'deleted': False}]})
    return JSONResponse(dumps(tmpbooks))

def get_book_by_id(user_id, book_id):
    if not isBookExist(user_id, book_id):
        return JSONResponse(jsonify({'message': "book %s not found." % (book_id)}), 404)
    tmpbooks = booksdb.find({'$and': [{'user_id': user_id}, {'book_id': book_id}]})
    return JSONResponse(dumps(tmpbooks))

def add_book(user_id,bookname, author="", publisher="", publish_date="", price="", ISBN="", tags=[], cover_image_url='http://i.imgur.com/zNPKpwk.jpg'):
    new_book_id = 1
    tmpbooks = booksdb.find().sort([('book_id', -1)]).limit(1)
    for book in tmpbooks:
        lastbook = book
    if lastbook['user_id'] is not None:
        new_book_id = int(lastbook['book_id'])+1
        
    tmpbook = {
        'book_id' : new_book_id,
        'bookname' : bookname,
        'author': author,
        'publisher': publisher,
        'publish_date': publish_date,
        'price': price,
        'ISBN': ISBN,
        'user_id': user_id,
        'tags': tags,
        'cover_image_url': cover_image_url,
        'deleted': False
    }

    booksdb.insert(tmpbook)
    print("User %s created a book, id=%s, bookname=\"%s\", author=\"%s\", publisher=\"%s\", publish_date=\"%s\", price=\"%s\", ISBN=\"%s\" tags=\"%s\"" \
          % (user_id, new_book_id, bookname, author, publisher, publish_date, price, ISBN, tags))
    return JSONResponse(dumps(tmpbook), 201)

def del_book(user_id, book_id):
    if not isBookExist(user_id, book_id):
        return JSONResponse(jsonify({'message': "book %s not found." % (book_id)}), 404)
    updateResult = booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'deleted': True}})
    print("User %s deleted book %s" % (user_id, book_id))
    #return JSONResponse(jsonify({'message': "Book %s deleted successful." % (book_id)}))
    return JSONResponse(updateResult)

def update_book(user_id, book_id, bookname="", author="", publisher="", publish_date="", price="", ISBN="", tags=[], cover_image_url=""):
    if not isBookExist(user_id, book_id):
        return JSONResponse(jsonify({'message': "book %s not found." % (book_id)}), 404)
    if bookname != "":
        booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'bookname': bookname}})
        log("Updated user %s's book %s's bookname to %s" % (user_id, book_id, bookname))
    if author != "":
        booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'author': author}})
        log("Updated user %s's book %s's author to %s" % (user_id, book_id, author))
    if publisher != "":
        booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'publisher': publisher}})
        log("Updated user %s's book %s's publisher to %s" % (user_id, book_id, publisher))
    if publish_date != "":
        booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'publish_date': publish_date}})
        log("Updated user %s's book %s's publish_date to %s" % (user_id, book_id, publish_date))
    if price != "":
        booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'price': price}})
        log("Updated user %s's book %s's price to %s" % (user_id, book_id, price))
    if ISBN != "":
        booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'ISBN': ISBN}})
        log("Updated user %s's book %s's ISBN to %s" % (user_id, book_id, ISBN))
    if tags:
        booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'tags': tags}})
        log("Updated user %s's book %s's tags to %s" % (user_id, book_id, tags))
    if cover_image_url != "":
        booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'cover_image_url': cover_image_url}})
        log("Updated user %s's book %s's cover_image_url to %s" % (user_id, book_id, cover_image_url))


    tmpbook = booksdb.find_one({'$and': [{'user_id': user_id}, {'book_id': book_id}]}) # Get updated data.
    return JSONResponse(dumps(tmpbook))