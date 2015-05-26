# coding=utf-8
from flask import Flask

from controllers.booksapi import booksapi
from controllers.usersapi import usersapi
from controllers.tokenapi import tokenapi
from controllers.loginapi import loginapi
from controllers.bookinfoapi import bookinfoapi
import sys

app = Flask(__name__)
app.register_blueprint(booksapi)
app.register_blueprint(usersapi)
app.register_blueprint(tokenapi)
app.register_blueprint(loginapi)
app.register_blueprint(bookinfoapi)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app.run(host='0.0.0.0', debug=True)
