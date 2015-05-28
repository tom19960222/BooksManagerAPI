from views.templates.JSONResponse import JSONResponse
from json import dumps
__author__ = 'Ikaros'
JSONREsponseTokenExpired = JSONResponse(dumps({'message': "Token expired"}), 403)
JSONResponseTokenNotFound = JSONResponse(dumps({'message': "Token not found."}), 404)
