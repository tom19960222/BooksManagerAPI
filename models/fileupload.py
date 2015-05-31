from werkzeug.utils import secure_filename
from flask import jsonify
from views.templates.JSONResponse import JSONResponse
from models.logger import log
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
BASE_URL = 'http://163.13.128.116:5001/'

def isAllowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def save_upload_file(file, user_id):
    if isAllowedFile(file.filename):
        if file is not None:
            UPLOAD_FOLDER = os.getcwd()+'/uploads/'+str(user_id)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            savepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
            log("User %s uploaded %s to %s" % (user_id, file.filename, savepath))
            file.save(savepath)
            return JSONResponse(jsonify({'cover_image_url': "%s%s/%s" % (BASE_URL, user_id, secure_filename(file.filename))}))
        else:
            return JSONResponse(jsonify({'message': "Null file provided."}), 400)
    else:
        return JSONResponse(jsonify({'message': 'Not allowed file format.'}), 400)
