from models.database import booksdb
def isBookExist(user_id, book_id):
    tmpbook = booksdb.find_one({'$and': [{'user_id': user_id}, {'book_id': book_id}]})
    if tmpbook is None:
        return False
    if len(tmpbook) == 0:
        return False
    return True
