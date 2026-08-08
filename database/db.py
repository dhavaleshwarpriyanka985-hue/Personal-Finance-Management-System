import sqlite3

db = sqlite3.connect("finance.db", check_same_thread=False)
db.row_factory = sqlite3.Row

cursor = db.cursor()