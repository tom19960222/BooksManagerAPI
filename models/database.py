from pymongo import MongoClient

dbClient = MongoClient('163.13.128.116', 27017)
db = dbClient.BooksManagerTest1
tokensdb = db.tokens
usersdb = db.users
booksdb = db.books
tagsdb = db.tags
categorysdb = db.categorys