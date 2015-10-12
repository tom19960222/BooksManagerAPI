from werkzeug.utils import secure_filename
from models.logger import log
from views.templates.JSONResponse import JSONResponse
from bson.json_util import dumps
from models.books import update_book
from models.users import update_user
import os
import json

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
BASE_URL = 'http://163.13.128.116:5001/'
COVER_IMAGES_SUBDIR = 'cover_images'
HEAD_IMAGE_SUBDIR = 'head_images'

def isAllowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def save_upload_file(file, user_id, subdir):
    if isAllowedFile(file.filename):
        if file is not None:
            UPLOAD_SUBFOLDER = str(user_id)+'/'+subdir
            UPLOAD_FOLDER = os.getcwd()+'/uploads'
            UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, UPLOAD_SUBFOLDER)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            savepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
            log("User %s uploaded %s to %s" % (user_id, secure_filename(file.filename), savepath))
            file.save(savepath)
            if subdir == COVER_IMAGES_SUBDIR:
                return JSONResponse(dumps({'cover_image_url': "%s%s/%s" % (BASE_URL, UPLOAD_SUBFOLDER, secure_filename(file.filename))}))
            else:
                return JSONResponse(dumps({'head_image_url': "%s%s/%s" % (BASE_URL, UPLOAD_SUBFOLDER, secure_filename(file.filename))}))
        else:
            return JSONResponse(dumps({'message': "Null file provided."}), 400)
    else:
        return JSONResponse(dumps({'message': 'Not allowed file format.'}), 400)

def save_book_cover_image(file, user_id, book_id):
    save_result = save_upload_file(file, user_id, COVER_IMAGES_SUBDIR)
    if save_result.status_code / 100 != 2:
        return save_result
    update_result = update_book(user_id, book_id, cover_image_url=json.loads(save_result.data)['cover_image_url'])
    if update_result.response_code / 100 != 2:
        return update_result
    return save_result

def save_user_head_image(file, user_id):
    save_result = save_upload_file(file, user_id, HEAD_IMAGE_SUBDIR)
    if save_result.status_code / 100 != 2:
        return save_result
    update_result = update_user(user_id, head_image_url=json.loads(save_result.data)['head_image_url'])
    if update_result.response_code / 100 != 2:
        return update_result
    return save_result