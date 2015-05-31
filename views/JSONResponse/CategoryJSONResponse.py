from views.templates.JSONResponse import JSONResponse
from bson.json_util import dumps

JSONResponseLoginFirst = JSONResponse(dumps({'message': 'Please log in first.'}), 401)