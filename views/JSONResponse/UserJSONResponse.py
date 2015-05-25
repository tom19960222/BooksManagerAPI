from json import dumps as jsonify
from views.templates.JSONRespons import JSONResponse
JSONResponseUserNotFound = JSONResponse(jsonify({'message': 'User not found.'}), 404)
JSONResponseUserLogoutSuccessful = JSONResponse(jsonify({'message': 'Logout successful'}), 200)