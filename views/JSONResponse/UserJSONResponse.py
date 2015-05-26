from json import dumps as jsonify
from views.templates.JSONResponse import JSONResponse
JSONResponseUserNotFound = JSONResponse(jsonify({'message': 'User not found.'}), 404)
JSONResponseUserLogoutSuccessful = JSONResponse(jsonify({'message': 'Logout successful'}), 200)
JSONResponseUserAlreadyExist = JSONResponse(jsonify({'message': 'User already exists.'}), 403)