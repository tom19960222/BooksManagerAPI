#!/usr/bin/python
# coding: UTF-8
from flask import Blueprint
import models.tokens

tokenapi = Blueprint('tokenapi', __name__, url_prefix='/api/token')

@tokenapi.route('', methods=["GET"])
def get_new_token():
    response = models.tokens.get_new_token()
    return response.response_message, response.response_code

@tokenapi.route('/<token>', methods=["GET"])
def get_token_by_token(token):
    response = models.tokens.get_token_by_token(token)
    return response.response_message, response.response_code
