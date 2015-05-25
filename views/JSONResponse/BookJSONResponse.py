from views.templates.JSONRespons import JSONResponse
from json import dumps as jsonify

JSONResponseProvideAtLeastBookName = JSONResponse(jsonify({'message': 'Please provide at least book name.'}), 400)
JSONResponseBookNotFound = JSONResponse(jsonify({'message': 'Can\'t found the book.'}), 404)