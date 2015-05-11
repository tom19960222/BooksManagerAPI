from database import tokensdb

def get_user_id_by_token(token):
    tmptoken = tokensdb.find_one({'token': token})
    return tmptoken['user_id']

