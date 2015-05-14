from json import dumps as jsonify
from views.templates.JSONResponse import JSONResponse
JSONResponseUserNotFound = JSONResponse(jsonify({'message': 'User not found.'}), 404)
