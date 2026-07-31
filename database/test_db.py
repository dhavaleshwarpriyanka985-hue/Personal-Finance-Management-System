import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="YOUR_PASSWORD",
        database="finance_db"
    )

    print("Database Connected Successfully!")

except Exception as e:
    print(e)