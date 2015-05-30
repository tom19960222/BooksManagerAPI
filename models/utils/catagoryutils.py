from models.database import catagorysdb


def isCatagoryExist(user_id, catagory_id):
    tmpcatagory = catagorysdb.find_one({'$and': [{'catagory_id': catagory_id}, {'user_id': user_id}]})
    if not tmpcatagory or len(tmpcatagory) == 0:
        return False
    return True