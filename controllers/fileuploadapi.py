from flask import Blueprint, request, abort
from werkzeug.utils import secure_filename
from models.fileupload import save_upload_file
from models.utils.userutils import get_user_id_by_token

fileuploadapi = Blueprint('fileuploadapi', __name__, url_prefix='/api/upload')

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

    return "%s%s" % (request.url_root, secure_filename(f.filename))
