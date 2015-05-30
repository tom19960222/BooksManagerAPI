from models.database import categorysdb


def isCatagoryExist(user_id, category_id):
    tmpcategory = categorysdb.find_one({'$and': [{'category_id': category_id}, {'user_id': user_id}]})
    if not tmpcategory or len(tmpcategory) == 0:
        return False
    return True