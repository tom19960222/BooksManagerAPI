#!/usr/bin/python
# coding: UTF-8
from flask import Blueprint
import models.utils.booksSearchAPI

bookinfoapi = Blueprint('bookinfoapi', __name__, url_prefix='/api/bookinfo')

@bookinfoapi.route('/<ISBN>', methods=["GET"])
def get_book_info(ISBN):
    response = models.utils.booksSearchAPI.getProductInfoByISBN(ISBN)
    return response.response_message, response.response_code