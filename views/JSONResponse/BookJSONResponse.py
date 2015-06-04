from views.templates.JSONResponse import JSONResponse
from bson.json_util import dumps

JSONResponseProvideAtLeastBookName = JSONResponse(dumps({'message': 'Please provide at least book name.'}), 400)
JSONResponseBookNotFound = JSONResponse(dumps({'message': 'Can\'t found the book.'}), 404)
JSONResponsePriceNotNumber = JSONResponse(dumps({'message': 'Price is not a number.'}), 400)