from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from views.JSONResponse.CommonJSONResponse import *
from views.templates.JSONResponse import makeResponse
from models.fileupload import save_book_cover_image, save_user_head_image
from models.utils.userutils import get_user_id_by_token

fileuploadapi = Blueprint('fileuploadapi', __name__, url_prefix='/api/upload')
BASE_URL = 'http://163.13.128.116:5001/'

@fileuploadapi.route('/book_cover_image/<int:book_id>', methods=['POST'])
def upload_file(book_id):
    token = request.headers.get('Token')
    if token is None:
        return makeResponse(JSONResponseProvideToken)

    user_id = get_user_id_by_token(token)
    if user_id == 0:
        return makeResponse(JSONResponseLoginFirst)
    if 'cover_image' not in request.files:
        return makeResponse(JSONResponse(dumps({'message': 'No cover_image provided.'}), 400))
    f = request.files['cover_image']
    save_result = save_book_cover_image(f, user_id, book_id)
    return save_result.response_message, save_result.response_code

@fileuploadapi.route('/user_head_image', methods=['POST'])
def upload_user_head():
    token = request.headers.get('Token')
    if token is None:
        return makeResponse(JSONResponseProvideToken)

    user_id = get_user_id_by_token(token)
    if user_id == 0:
        return makeResponse(JSONResponseLoginFirst)
    if 'head_image' not in request.files:
        return makeResponse(JSONResponse(dumps({'message': 'No head_image provided.'}), 400))
    f = request.files['head_image']
    saveresult = save_user_head_image(f, user_id)
    return saveresult.response_message, saveresult.response_code