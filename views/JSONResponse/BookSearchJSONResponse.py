from views.templates.JSONResponse import JSONResponse
from json import dumps
__author__ = 'Ikaros'
JSONResponseISBNNotFound = JSONResponse(dumps({'message': "ISBN not found"}), 404)
JSONResponsePicNotFound = JSONResponse(dumps({'message': "Pic not found"}), 404)

