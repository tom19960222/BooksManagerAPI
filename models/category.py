#!/usr/bin/python
#coding: UTF-8

from flask import jsonify
from bson.json_util import dumps
from models.logger import log
from database import categorysdb
from views.templates.JSONResponse import JSONResponse
from utils.categoryutils import isCatagoryExist
from utils.bookutils import isBookExist

category = [
    {
        'category_id': 1,
        'category_name': "GuanGuan\'s favorite",
        'user_id': 1,
        'book_list': [1, 3, 5],
        'deleted': False
    }
]

def list_all_category(user_id):
    tmpcategorys = categorysdb.find({'$and': [{'user_id': user_id}, {'deleted': False}]})
    return JSONResponse(dumps(tmpcategorys))

def get_category_by_id(user_id, category_id):
    if not isCatagoryExist(user_id, category_id):
        return JSONResponse(jsonify({'message': "category %s not found." % (category_id)}), 404)
    tmpbooks = categorysdb.find({'$and': [{'user_id': user_id}, {'category_id': category_id}]})
    return JSONResponse(dumps(tmpbooks))

def add_category(user_id, category_name):
    oldCatagory = categorysdb.find_one({'$and': [{'user_id': user_id}, {'category_name': category_name}, {'deleted': False}]})
    if oldCatagory is not None:
        return JSONResponse(jsonify({'message': "Catagory %s already exist." % category_name}))

    new_category_id = 1
    lastcata = dict()
    lastcata['category_id'] = 1
    tmpcatas = categorysdb.find().sort([('category_id', -1)]).limit(1)
    for cata in tmpcatas:
        lastcata = cata
    if lastcata['category_id'] is not None:
        new_category_id = int(lastcata['category_id'])+1

    category = [
        {
            'category_id': new_category_id,
            'category_name': category_name,
            'user_id': user_id,
            'book_list': [],
            'deleted': False
        }
    ]

    categorysdb.insert(category)
    log("User %s created a category, category_id = %s , category_name = %s" % (user_id, new_category_id, category_name))
    return JSONResponse(dumps(category), 201)

def add_books_to_category(user_id, category_id, book_list_or_int):
    if type(book_list_or_int) is list:
        for book_id in book_list_or_int:
            if not isBookExist(user_id, book_id):
                return JSONResponse(jsonify({'message': 'User %s doesn\'t own book %s' % (user_id, book_id)}))
        categorysdb.update({'$and': [{'user_id': user_id}, {'category_id': category_id}]}, {'$addToSet': {'book_list': {'$each': book_list_or_int}}})
    else:
        if not isBookExist(user_id, book_list_or_int):
            return JSONResponse(jsonify({'message': 'User %s doesn\'t own book %s' % (user_id, book_list_or_int)}))
        categorysdb.update({'$and': [{'user_id': user_id}, {'category_id': category_id}]}, {'$addToSet': {'book_list': book_list_or_int}})
    tmpcategory = categorysdb.find_one({'$and': [{'user_id': user_id}, {'category_id': category_id}]})
    log("User %s added books %s to category %s" % (user_id, book_list_or_int, category_id))
    return JSONResponse(dumps(tmpcategory), 200)

def del_category(user_id, category_id):
    if not isCatagoryExist(user_id, category_id):
        return JSONResponse(jsonify({'message': "category %s not found." % category_id}), 404)
    updateResult = categorysdb.update({'$and': [{'user_id': user_id}, {'category_id': category_id}]}, {'$set': {'deleted': True}})
    log("User %s deleted category %s" % (user_id, category_id))
    return JSONResponse(updateResult)


def del_books_from_category(user_id, category_id, book_int_or_list):
    delresult = None
    if not isCatagoryExist(user_id, category_id):
        return JSONResponse(jsonify({'message': "category %s not found." % category_id}), 404)
    if type(book_int_or_list) is int:
        delresult = categorysdb.update({'$and': [{'user_id': user_id}, {'category_id': category_id}]}, {'$pull': {'book_list': book_int_or_list}})
    elif type(book_int_or_list) is list:
        delresult = categorysdb.update({'$and': [{'user_id': user_id}, {'category_id': category_id}]}, {'$pullAll': {'book_list': book_int_or_list}})
    else:
        return JSONResponse(jsonify({'message': 'Please provide correct data format.'}), 400)
    return JSONResponse(dumps(delresult))


def update_category(user_id, cataogry_id, category_name=""):
    if not isCatagoryExist(user_id, cataogry_id):
        return JSONResponse(jsonify({'message': "category %s not found." % (cataogry_id)}), 404)
    updated = None
    if category_name != "":
        updated = categorysdb.update({'$and': [{'user_id': user_id}, {'category_id': cataogry_id}]}, {'$set': {'category_name': category_name}})
        if updated is not None:
            log("Updated user %s's category %s's category_name to %s" % (user_id, cataogry_id, category_name))
    tmpbook = categorysdb.find_one({'$and': [{'user_id': user_id}, {'category_id': cataogry_id}]}) # Get updated data.
    return JSONResponse(dumps(tmpbook))