from flask import jsonify
from bson.json_util import dumps

class JSONResponse:
    def __init__(self, response_dict_or_string="", response_code=200):
        if type(response_dict_or_string) is dict:
            self.response_message = dumps(response_dict_or_string)
        else:
            self.response_message = response_dict_or_string
        self.response_code = response_code
        print("Created JSON response, return code=%s, message=%s" % (self.response_code, self.response_message))

    def makeJSONResponse(self):
        if type(self.response_message) is dict:
            return str(dumps(self.response_message))
        return str(self.response_message)

    def __str__(self):
        return "%s: %s" % (self.response_code, self.response_message)