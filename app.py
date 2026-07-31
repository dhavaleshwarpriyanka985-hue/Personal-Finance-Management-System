from flask import Flask

app = Flask(__name__)

# Secret Key
app.secret_key = "your_secret_key"

# Import all routes
from routes.auth import *
from routes.finance import *
from routes.ai import *
from routes.report import *
from app import app

if __name__ == "__main__":
    app.run(debug=True)