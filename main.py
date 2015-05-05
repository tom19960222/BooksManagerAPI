# coding=utf-8
from flask import Flask
from booksapi import booksapi
from tagsapi import tagsapi
from usersapi import usersapi
from tokenapi import tokenapi
from pymongo import MongoClient

app = Flask(__name__)
app.register_blueprint(booksapi)
app.register_blueprint(tagsapi)
app.register_blueprint(usersapi)
app.register_blueprint(tokenapi)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
