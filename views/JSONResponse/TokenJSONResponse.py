from views.templates.JSONResponse import JSONResponse
from flask import jsonify
__author__ = 'Ikaros'
JSONREsponseTokenExpired = JSONResponse(jsonify({'message': "Token expired"}), 403)
