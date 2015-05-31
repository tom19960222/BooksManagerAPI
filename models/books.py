#!/usr/bin/python
#coding: UTF-8
from flask import jsonify
from bson.json_util import dumps
from models.logger import log
from database import booksdb
from views.templates.JSONResponse import JSONResponse
from utils.bookutils import isBookExist
from category import *
from fileupload import save_upload_file
import time, json

books = {
        'book_id': 0,
        'bookname': u'雨港基隆 - 桐花雨',
        'author': u'東方紅',
        'publisher': u'尖端出版',
        'publish_date': '20150101',
        'price': 200,
        'ISBN': '1234567890',
        'tags': ['QQ', 'QQQ'],
        'cover_images_url': 'http://i.imgur.com/zNPKpwk.jpg',
        'user_id': 1,
        'create_time': 1,
        'update_time': 1,
        'category_id': [4, 5]
    }

def list_all_books(user_id):
    tmpbooks = booksdb.find({'$and': [{'user_id': user_id}, {'deleted': False}]})
    bookscategories = categorysdb.find({'$and': [{'user_id': user_id}, {'deleted': False}]})
    booksjson = json.loads(dumps(tmpbooks))
    categoiesjson = json.loads(dumps(bookscategories))
    for book in booksjson:
        book['category_id'] = list()
        for category in categoiesjson:
            if book['book_id'] in category['book_list']:
                book['category_id'].append(category['category_id'])
    return JSONResponse(dumps(booksjson))

def get_book_by_id(user_id, book_id):
    if not isBookExist(user_id, book_id):
        return JSONResponse(jsonify({'message': "book %s not found." % (book_id)}), 404)
    tmpbook = booksdb.find_one({'$and': [{'user_id': user_id}, {'book_id': book_id}]})
    bookscategories = categorysdb.find({'$and': [{'user_id': user_id}, {'deleted': False}, {'book_list': book_id}]})
    book = json.loads(dumps(tmpbook))
    categoiesjson = json.loads(dumps(bookscategories))
    book['category_id'] = list()
    for category in categoiesjson:
        book['category_id'].append(category['category_id'])
    return JSONResponse(book)

def add_book(user_id,bookname, author="", publisher="", publish_date="", price="", ISBN="", tags=[],
             cover_image_url='http://i.imgur.com/zNPKpwk.jpg', category=[], cover_image=""):
    new_book_id = 1
    tmpbooks = booksdb.find().sort([('book_id', -1)]).limit(1)
    for book in tmpbooks:
        lastbook = book
    if lastbook['user_id'] is not None:
        new_book_id = int(lastbook['book_id'])+1
    nowtime = time.time()

    tmpbook = {
        'book_id': new_book_id,
        'bookname': bookname,
        'author': author,
        'publisher': publisher,
        'publish_date': publish_date,
        'price': price,
        'ISBN': ISBN,
        'user_id': user_id,
        'tags': tags,
        'cover_image_url': cover_image_url,
        'deleted': False,
        'create_time': nowtime,
        'update_time': nowtime,
    }
    if cover_image != "":
        save_result = save_upload_file(cover_image, user_id)
        if save_result.response_code / 100 != 2:
            return save_result
        else:
            tmpbook['cover_image_url'] = (json.loads(save_result.response_message))['cover_image_url']
    booksdb.insert(tmpbook)
    if type(category) is list:
        addresult = JSONResponse()
        for category_id in category:
            addresult = add_books_to_category(user_id, category_id, new_book_id)
    elif type(category) is int:
        addresult = add_books_to_category(user_id, category, new_book_id)
    if int(addresult.response_code)/100 != 2:
            return addresult


    if type(category) is list:
        tmpbook['category_id'] = category # category data is stored in categorysdb, so it is not inserted to booksdb.
    elif type(category) is int:
        tmpbook['category_id'] = list()
        tmpbook['category_id'].append(category)
    log("User %s created a book, id=%s, bookname=\"%s\", author=\"%s\", publisher=\"%s\", publish_date=\"%s\", price=\"%s\", ISBN=\"%s\" tags=\"%s\", create_time=\"%s\", update_time=\"%s\", categoey=\"%s\""
          % (user_id, new_book_id, bookname, author, publisher, publish_date, price, ISBN, tags, nowtime, nowtime, category))
    return JSONResponse(dumps(tmpbook), 201)

def del_book(user_id, book_id):
    if not isBookExist(user_id, book_id):
        return JSONResponse(jsonify({'message': "book %s not found." % (book_id)}), 404)
    allcategories = categorysdb.find({'$and': [{'user_id': user_id}, {'book_list': book_id}]})
    for category in allcategories:
        del_books_from_category(user_id, category['category_id'], book_id)
    updateResult = booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'deleted': True}})
    log("User %s deleted book %s" % (user_id, book_id))
    return JSONResponse(updateResult)

def update_book(user_id, book_id, bookname="", author="", publisher="", publish_date="", price="", ISBN="", tags=[], cover_image_url=""):
    if not isBookExist(user_id, book_id):
        return JSONResponse(jsonify({'message': "book %s not found." % (book_id)}), 404)
    updated = 0
    if bookname != "":
        updated = booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'bookname': bookname}})
        log("Updated user %s's book %s's bookname to %s" % (user_id, book_id, bookname))
    if author != "":
        updated = booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'author': author}})
        log("Updated user %s's book %s's author to %s" % (user_id, book_id, author))
    if publisher != "":
        updated = booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'publisher': publisher}})
        log("Updated user %s's book %s's publisher to %s" % (user_id, book_id, publisher))
    if publish_date != "":
        updated = booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'publish_date': publish_date}})
        log("Updated user %s's book %s's publish_date to %s" % (user_id, book_id, publish_date))
    if price != "":
        updated = booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'price': price}})
        log("Updated user %s's book %s's price to %s" % (user_id, book_id, price))
    if ISBN != "":
        updated = booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'ISBN': ISBN}})
        log("Updated user %s's book %s's ISBN to %s" % (user_id, book_id, ISBN))
    if tags:
        updated = booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'tags': tags}})
        log("Updated user %s's book %s's tags to %s" % (user_id, book_id, tags))
    if cover_image_url != "":
        updated = booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'cover_image_url': cover_image_url}})
        log("Updated user %s's book %s's cover_image_url to %s" % (user_id, book_id, cover_image_url))
    # if category:
    #     updated = booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'category': category}})
    #     log("Updated user %s's book %s's category to %s" % (user_id, book_id, category))
    if updated:
        nowtime = time.time()
        booksdb.update({'$and': [{'user_id': user_id}, {'book_id': book_id}]}, {'$set': {'update_time': nowtime}})
        log("Updated user %s's book %s's update_time to %s" % (user_id, book_id, nowtime))

    # tmpbook = booksdb.find_one({'$and': [{'user_id': user_id}, {'book_id': book_id}]}) # Get updated data.
    return get_book_by_id(user_id, book_id)