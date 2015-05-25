from json import dumps as jsonify
from views.templates.JSONResponse import JSONResponse
JSONResponseProvideNecessaryInfo = JSONResponse(jsonify({'message': 'Please provide all necessary info.'}), 400)
JSONResponseLoginSuccessful = JSONResponse(jsonify({'message': "Login successful"}))
JSONResponseWrongPassword = JSONResponse(jsonify({'message': "Wrong password."}), 403)
