from views.templates.JSONRespons import JSONResponse
from json import dumps as jsonify

JSONResponseLoginFirst = JSONResponse(jsonify({'message': 'Please log in first.'}), 401)
JSONResponseProvideToken = JSONResponse(jsonify({'message': 'Please provide token.'}), 401)
JSONResponseInvalidJSON = JSONResponse(jsonify({'message': 'Invalid JSON request.'}), 400)
