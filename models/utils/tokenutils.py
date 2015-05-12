from models.database import tokensdb


def change_token_user(token, user_id):
    tokensdb.update({'token': token}, {'$set': {'user_id': user_id}})

def get_token_expire_time(token):
    tmptoken = tokensdb.find_one({'token': token})
    return tmptoken['expire_time']