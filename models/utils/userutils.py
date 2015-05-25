from models.database import tokensdb
from models.utils.tokenutils import isTokenExpired

def get_user_id_by_token(token):
    tmptoken = tokensdb.find_one({'token': token})
    if not tmptoken:
        return 0
    if len(tmptoken) == 0:
        return 0
    return tmptoken['user_id']

def checkIsVaildUserWithToken(token):
    tmpuserid = get_user_id_by_token(token)
    if tmpuserid == 0:
        return False
    return True