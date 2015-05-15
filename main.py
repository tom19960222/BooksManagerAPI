# coding=utf-8
from flask import Flask

from controllers.booksapi import booksapi
from controllers.usersapi import usersapi
from controllers.tokenapi import tokenapi
from controllers.loginapi import loginapi


app = Flask(__name__)
app.register_blueprint(booksapi)
app.register_blueprint(usersapi)
app.register_blueprint(tokenapi)
app.register_blueprint(loginapi)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
