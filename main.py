# coding=utf-8
from flask import Flask
from booksapi import booksapi
from tagsapi import tagsapi
from usersapi import usersapi

app = Flask(__name__)
app.register_blueprint(booksapi)
app.register_blueprint(tagsapi)
app.register_blueprint(usersapi)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
