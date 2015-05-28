from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from views.JSONResponse.CommonJSONResponse import *
from views.templates.JSONResponse import makeResponse
from models.fileupload import save_upload_file
from models.utils.userutils import get_user_id_by_token

fileuploadapi = Blueprint('fileuploadapi', __name__, url_prefix='/api/upload')
BASE_URL = 'http://163.13.128.116:5001/'

@fileuploadapi.route('', methods=['POST'])
def upload_file():
    token = request.headers.get('Token')
    if token is None:
        return makeResponse(JSONResponseProvideToken)

    user_id = get_user_id_by_token(token)
    if user_id == 0:
        return makeResponse(JSONResponseLoginFirst)
    print("%s: %s" % (token, user_id))
    f = request.files['cover_image']
    save_upload_file(f, user_id)

    return jsonify({'cover_image_url': "%s%s/%s" % (BASE_URL, user_id, secure_filename(f.filename))})
