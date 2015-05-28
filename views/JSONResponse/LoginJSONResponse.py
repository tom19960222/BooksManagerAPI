from json import dumps
from views.templates.JSONResponse import JSONResponse
JSONResponseProvideNecessaryInfo = JSONResponse(dumps({'message': 'Please provide all necessary info.'}), 400)
JSONResponseLoginSuccessful = JSONResponse(dumps({'message': "Login successful"}))
JSONResponseWrongPassword = JSONResponse(dumps({'message': "Wrong password."}), 403)
