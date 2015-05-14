from views.templates.JSONResponse import JSONResponse
from flask import jsonify

JSONResponseLoginFirst = JSONResponse(jsonify({'message': 'Please log in first.'}), 401)
JSONResponseProvideToken = JSONResponse(jsonify({'message': 'Please provide token.'}), 401)
JSONResponseInvalidJSON = JSONResponse(jsonify({'message': 'Invalid JSON request.'}), 400)
