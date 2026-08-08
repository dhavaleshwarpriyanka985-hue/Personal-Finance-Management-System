import os

DB_HOST = os.environ.get("MYSQLHOST", "localhost")
DB_USER = os.environ.get("MYSQLUSER", "root")
DB_PASSWORD = os.environ.get("MYSQLPASSWORD", "MySQL@123")
DB_NAME = os.environ.get("MYSQLDATABASE", "finance_db")
DB_PORT = int(os.environ.get("MYSQLPORT", 3307))

SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")