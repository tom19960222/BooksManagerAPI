from views.templates.JSONResponse import JSONResponse
from json import dumps as jsonify
__author__ = 'Ikaros'
JSONResponseISBNNotFound = JSONResponse(jsonify({'message': "ISBN not found"}), 404)
JSONResponsePicNotFound = JSONResponse(jsonify({'message': "Pic not found"}), 404)

