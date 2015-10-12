from bson.json_util import dumps
from models.logger import log
import flask


def makeResponse(JSONResponse):
    return JSONResponse

class JSONResponse(flask.Response):
    def __init__(self, response_dict_or_string="", response_code=200):
        flask.Response.__init__(self)
        if type(response_dict_or_string) is dict:
            self.data = dumps(response_dict_or_string)
        elif type(response_dict_or_string) is list:
            self.data = dumps(response_dict_or_string)
        else:
            self.data = response_dict_or_string
        self.status_code = response_code
        log("Created JSON response, return code=%s, message=%s" % (self.status_code, self.data))
        self.headers['Access-Control-Allow-Origin'] = '*'

    def makeJSONResponse(self):
        if type(self.data) is dict:
            return dumps(self.data)
        return self.data

    def __str__(self):
        return "%s: %s" % (self.status_code, self.data)