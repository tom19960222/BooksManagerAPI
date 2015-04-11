#!/usr/bin/python
# coding: UTF-8
from flask import Blueprint, jsonify, abort, request

tagsapi = Blueprint('tagsapi', __name__, url_prefix='/api/tag')

tags = [
    {
    'tag_id': 0,
	'ISBN' : '1234567890',
	'tags' : '輕小說',
	'user_id' : 0
    }
]

@tagsapi.route('', methods=['GET'])
def list_all_tags():
    return jsonify({'tags': tags})


@tagsapi.route('/<int:tag_id>', methods=['GET'])
def get_tag_by_id(tag_id):
    tmptags = [tmptag for tmptag in tags if tmptag['tag_id'] == tag_id]
    if len(tmptags) == 0:
        abort(404)
    return jsonify({'tags': tmptags[0]})


@tagsapi.route('', methods=['POST'])
def add_tag():
    jsondata = request.get_json()
    if not jsondata or not 'ISBN' in jsondata or not 'user_id' in jsondata or not 'tags' in jsondata:
        abort(400)

    tmptaglist = list()
    for tag in jsondata['tags']:
        tmptaglist.append(tag)
    tagAvaliable = [tag for tag in tags if tag['user_id'] == jsondata['user_id'] and tag['ISBN'] == jsondata['ISBN']]
    if not tagAvaliable:
        tmptag = {
            'tag_id': tags[-1]['tag_id'] + 1,
            'user_id': jsondata['user_id'],
            'ISBN': jsondata['ISBN'],
            'tags': tmptaglist
        }
        tags.append(tmptag)
        return jsonify({'tags':tmptag}), 201
    else:
        for tag in tmptaglist:
            if tag not in tagAvaliable[0]['tags']:
                tagAvaliable[0]['tags'].append(tag)
        return jsonify({'tags':tagAvaliable[0]}), 201

@tagsapi.route('', methods=['DELETE'])
def del_tag():
    jsondata = request.get_json()
    tmptag = [tmptag for tmptag in tags if tmptag['ISBN'] == jsondata['ISBN']]
    if len(tmptag) == 0:
        abort(404)
    for tag in jsondata['tags']:
        if tag in tmptag[0]['tags']:
            tmptag[0]['tags'].remove(tag)

    return jsonify({'result': True})


"""
@tagsapi.route('', methods=['PUT'])
def update_tag(ISBN):
    tmptag = [tmptag for tmptag in tags if tmptag['ISBN'] == ISBN]
    jsondata = request.get_json()
    if len(tmptag) == 0:
        abort(404)
    if not jsondata:
        abort(400)

    if 'password' in request.json and type(request.json['password']) is unicode:
        tmptag[0]['password'] = jsondata['password']
        return jsonify({'book': tmptag[0]})
"""