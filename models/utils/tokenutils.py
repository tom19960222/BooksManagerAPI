from models.database import tokensdb
import random
import string


def changeTokenUser(token, user_id):
    tokensdb.update({'token': token}, {'$set': {'user_id': user_id}})

def getTokenExpireTime(token):
    tmptoken = tokensdb.find_one({'token': token})
    return tmptoken['expire_time']

def generateAccessToken():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))