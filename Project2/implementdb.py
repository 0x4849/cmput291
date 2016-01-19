import bsddb
DATABASE = "cstudents2.db"
db = bsddb.btopen(DATABASE,'c') # Creates B-Tree DB
print(db.keys())

