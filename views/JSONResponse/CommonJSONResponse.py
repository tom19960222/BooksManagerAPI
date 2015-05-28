from views.templates.JSONResponse import JSONResponse
from json import dumps

JSONResponseLoginFirst = JSONResponse(dumps({'message': 'Please log in first.'}), 401)
JSONResponseProvideToken = JSONResponse(dumps({'message': 'Please provide token.'}), 401)
JSONResponseInvalidJSON = JSONResponse(dumps({'message': 'Invalid JSON request.'}), 400)
