from views.templates.JSONResponse import JSONResponse
from json import dumps as jsonify
__author__ = 'Ikaros'
JSONREsponseTokenExpired = JSONResponse(jsonify({'message': "Token expired"}), 403)
