from utils.tokenutils import *
from models.database import tokensdb
from models.logger import log
from views.templates.JSONResponse import makeResponse
from views.JSONResponse.TokenJSONResponse import *
from views.JSONResponse.CommonJSONResponse import *
from bson.json_util import dumps

access_tokens = [
    {
	'token' : 'fjrubrifgkdjnidjvisdjoj',
	'user_id' : 0,
	'expire_time' : 1429867579
    }
]

expire_seconds = 86400

def get_new_token():
    randomToken = generateAccessToken()
    expire_time = int(time.time()) + expire_seconds
    tmptoken = {
        'token': randomToken,
        'user_id': 0,
        'expire_time': expire_time
    }
    tokensdb.insert_one(tmptoken)
    log("Token %s generated, expired when %s seconds" % (randomToken, expire_time))
    return JSONResponse(dumps(tmptoken), 201)

def getTokenInfoByToken(token):
    if token == "ALL":
        tmptoken = tokensdb.find()
    else:
        tmptoken = tokensdb.find_one({'token': token})
        if len(tmptoken) == 0:
            return makeResponse(JSONResponseTokenNotFound)
    return JSONResponse(dumps(tmptoken))

def isErrorToken(token):
    if not token:
        return JSONResponseProvideToken
    if not isTokenExist(token):
        return JSONResponseTokenNotFound
    if isTokenExpired(token):
        return JSONREsponseTokenExpired
    return None