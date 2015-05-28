from json import dumps
from views.templates.JSONResponse import JSONResponse
JSONResponseUserNotFound = JSONResponse(dumps({'message': 'User not found.'}), 404)
JSONResponseUserLogoutSuccessful = JSONResponse(dumps({'message': 'Logout successful'}), 200)
JSONResponseUserAlreadyExist = JSONResponse(dumps({'message': 'User already exists.'}), 403)
JSONResponseUserDeactivated = JSONResponse(dumps({'message': 'User already deleted.'}), 403)