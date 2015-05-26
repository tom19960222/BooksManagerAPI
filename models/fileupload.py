from werkzeug.utils import secure_filename
from models.logger import log
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def isAllowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def save_upload_file(file, user_id):
    if file is not None and isAllowedFile(file.filename):
        UPLOAD_FOLDER = os.getcwd()+'/uploads/'+str(user_id)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        savepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        log("User %s uploaded %s to %s" % (user_id, file.filename, savepath))
        file.save(savepath)
