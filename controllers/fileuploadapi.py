from flask import Blueprint, request
from werkzeug.utils import secure_filename
import os

fileuploadapi = Blueprint('fileuploadapi', __name__, url_prefix='/api/upload')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = os.getcwd()+'/uploads'


def isAllowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@fileuploadapi.route('', methods=['POST'])
def upload_file():
    f = request.files['cover_image']
    
    f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
    return UPLOAD_FOLDER
