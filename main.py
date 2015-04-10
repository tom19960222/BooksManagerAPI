# coding=utf-8
from flask import Flask
from booksapi import booksapi

app = Flask(__name__)
app.register_blueprint(booksapi)
"""
books = [
    {
	'book_id' : 0,
	'bookname' : '雨港基隆 - 桐花雨',
	'author' : '東方紅',
	'publisher' : '尖端出版',
	'publish_date' : '20150101',
	'price' : 200,
	'ISBN' : '1234567890'
    }
]
"""
users = [
    {
	'user_id' : 0,
	'username' : 'Ananymous',
	'email' : '',
	'password' : '',
	'lastlogintime' : '20150408 15:59',
	'lastloginip' : '127.0.0.1'
    }
]

access_tokens = [
    {
	'token' : 'fjrubrifgkdjnidjvisdjoj',
	'user_id' : 0,
	'expire_time' : '20150409 15:59'
    } 
]

tags = [
    {
	'ISBN' : '1234567890',
	'tags' : '輕小說',
	'user_id' : 0
    }
]

"""
@app.route('/api/list', methods=['POST'])
def add_list():
    if not request.json or not 'content' in request.json:
        abort(400);
    listtmp = {
        'id' : lists[-1]['id']+1,
        'content' : request.json['content']
    }
    lists.append(listtmp)
    return jsonify({'list':listtmp}), 201

@app.route('/api/list/<int:list_id>', methods=['DELETE'])
def del_list(list_id):
    listtmp = [tmp for tmp in lists if tmp['id'] == list_id]
    if len(listtmp) == 0:
        abort(404)
    lists.remove(listtmp[0])
    return jsonify({'result':True})

@app.route('/api/list/<int:list_id>', methods=['PUT'])
def update_list(list_id):
    listtmp = [tmp for tmp in lists if tmp['id'] == list_id]
    if len(listtmp) == 0:
        abort(404)
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
