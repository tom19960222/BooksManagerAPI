from models.database import tokensdb
import random
import string


def changeTokenUser(token, user_id):
    tokensdb.update({'token': token}, {'$set': {'user_id': user_id}})

def getTokenExpireTime(token):
    tmptoken = tokensdb.find_one({'token': token})
    if tmptoken is None:
        return 0
    if len(tmptoken) == 0:
        return 0
    return tmptoken['expire_time']

def generateAccessToken():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))

def isValidToken(token):
    tmptoken = tokensdb.find_one({'token': token})
    if tmptoken is None:
        return False
    if len(tmptoken) == 0:
        return False
    return True