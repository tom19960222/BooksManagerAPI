#!/usr/bin/python
#coding: UTF-8

from flask import jsonify
from bson.json_util import dumps
from models.logger import log
from database import catagorysdb
from views.templates.JSONResponse import JSONResponse
from utils.catagoryutils import isCatagoryExist
from utils.bookutils import isBookExist

catagory = [
    {
        'catagory_id': 1,
        'catagory_name': "GuanGuan\'s favorite",
        'user_id': 1,
        'book_list': [1, 3, 5],
        'deleted': False
    }
]

def list_all_catagory(user_id):
    tmpcatagorys = catagorysdb.find({'$and': [{'user_id': user_id}, {'deleted': False}]})
    return JSONResponse(dumps(tmpcatagorys))

def get_catagory_by_id(user_id, catagory_id):
    if not isCatagoryExist(user_id, catagory_id):
        return JSONResponse(jsonify({'message': "catagory %s not found." % (catagory_id)}), 404)
    tmpbooks = catagorysdb.find({'$and': [{'user_id': user_id}, {'catagory_id': catagory_id}]})
    return JSONResponse(dumps(tmpbooks))

def add_catagory(user_id, catagory_name):
    oldCatagory = catagorysdb.find_one({'$and': [{'user_id': user_id}, {'catagory_name': catagory_name}, {'deleted': False}]})
    if oldCatagory is not None:
        return JSONResponse(jsonify({'message': "Catagory %s already exist." % catagory_name}))

    new_catagory_id = 1
    tmpcatas = catagorysdb.find().sort([('catagory_id', -1)]).limit(1)
    for cata in tmpcatas:
        lastcata = cata
    if lastcata['user_id'] is not None:
        new_catagory_id = int(lastcata['catagory_id'])+1

    catagory = [
        {
            'catagory_id': new_catagory_id,
            'catagory_name': catagory_name,
            'user_id': user_id,
            'book_list': [],
            'deleted': False
        }
    ]

    catagorysdb.insert(catagory)
    log("User %s created a catagory, catagory_id = %s , catagory_name = %s" % (user_id, new_catagory_id, catagory_name))
    return JSONResponse(dumps(catagory), 201)

def add_books_to_catagory(user_id, catagory_id, book_list_or_int):
    if type(book_list_or_int) is list:
        for book_id in book_list_or_int:
            if not isBookExist(user_id, book_id):
                return JSONResponse(jsonify({'message': 'User %s doesn\'t own book %s' % (user_id, book_id)}))
        catagorysdb.update({'$and': [{'user_id': user_id}, {'catagory_id': catagory_id}]}, {'$addToSet': {'book_list': {'$each': book_list_or_int}}})
    else:
        if not isBookExist(user_id, book_list_or_int):
            return JSONResponse(jsonify({'message': 'User %s doesn\'t own book %s' % (user_id, book_list_or_int)}))
        catagorysdb.update({'$and': [{'user_id': user_id}, {'catagory_id': catagory_id}]}, {'$addToSet': {'book_list': book_list_or_int}})
    tmpcatagory = catagorysdb.find_one({'$and': [{'user_id': user_id}, {'catagory_id': catagory_id}]})
    log("User %s added books %s to catagory %s" % (user_id, book_list_or_int, catagory_id))
    return JSONResponse(dumps(tmpcatagory), 200)

def del_catagory(user_id, catagory_id):
    if not isCatagoryExist(user_id, catagory_id):
        return JSONResponse(jsonify({'message': "catagory %s not found." % catagory_id}), 404)
    updateResult = catagorysdb.update({'$and': [{'user_id': user_id}, {'catagory_id': catagory_id}]}, {'$set': {'deleted': True}})
    log("User %s deleted catagory %s" % (user_id, catagory_id))
    return JSONResponse(updateResult)


def del_books_from_catagory(user_id, catagory_id, book_int_or_list):
    delresult = None
    if not isCatagoryExist(user_id, catagory_id):
        return JSONResponse(jsonify({'message': "catagory %s not found." % catagory_id}), 404)
    if type(book_int_or_list) is int:
        delresult = catagorysdb.update({'$and': [{'user_id': user_id}, {'catagory_id': catagory_id}]}, {'$pull': {'book_list': book_int_or_list}})
    elif type(book_int_or_list) is list:
        delresult = catagorysdb.update({'$and': [{'user_id': user_id}, {'catagory_id': catagory_id}]}, {'$pullAll': {'book_list': book_int_or_list}})
    else:
        return JSONResponse(jsonify({'message': 'Please provide correct data format.'}), 400)
    return JSONResponse(dumps(delresult))


def update_catagory(user_id, cataogry_id, catagory_name=""):
    if not isCatagoryExist(user_id, cataogry_id):
        return JSONResponse(jsonify({'message': "catagory %s not found." % (cataogry_id)}), 404)
    updated = None
    if catagory_name != "":
        updated = catagorysdb.update({'$and': [{'user_id': user_id}, {'catagory_id': cataogry_id}]}, {'$set': {'catagory_name': catagory_name}})
        if updated is not None:
            log("Updated user %s's catagory %s's catagory_name to %s" % (user_id, cataogry_id, catagory_name))
    tmpbook = catagorysdb.find_one({'$and': [{'user_id': user_id}, {'catagory_id': cataogry_id}]}) # Get updated data.
    return JSONResponse(dumps(tmpbook))