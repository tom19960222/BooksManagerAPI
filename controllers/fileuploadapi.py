from flask import Blueprint, request, abort
from werkzeug.utils import secure_filename
from models.fileupload import save_upload_file
from models.utils.userutils import get_user_id_by_token

fileuploadapi = Blueprint('fileuploadapi', __name__, url_prefix='/api/upload')
BASE_URL = 'http://163.13.128.116:5001/'

@fileuploadapi.route('', methods=['POST'])
def upload_file():
    token = request.headers.get('Token')
    if token is None:
        abort(400)
    user_id = get_user_id_by_token(token)
    if user_id == 0:
        abort(403)
    print("%s: %s" % (token, user_id))
    f = request.files['cover_image']
    save_upload_file(f, user_id)

    return "%s%s/%s" % (BASE_URL, user_id, secure_filename(f.filename))
