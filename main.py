# coding=utf-8
from flask import Flask

from booksapi import booksapi
from controllers import tagsapi
from usersapi import usersapi
from tokenapi import tokenapi
from loginapi import loginapi


app = Flask(__name__)
app.register_blueprint(booksapi)
app.register_blueprint(tagsapi)
app.register_blueprint(usersapi)
app.register_blueprint(tokenapi)
app.register_blueprint(loginapi)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
