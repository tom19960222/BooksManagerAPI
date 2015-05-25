from views.templates.JSONRespons import JSONResponse
from json import dumps as jsonify
__author__ = 'Ikaros'
JSONREsponseTokenExpired = JSONResponse(jsonify({'message': "Token expired"}), 403)
JSONResponseTokenNotFound = JSONResponse(jsonify({'message': "Token not found."}), 404)
