from flask import Flask, redirect
from routes.report import report_bp

app = Flask(__name__)

app.register_blueprint(report_bp)

app.secret_key = "your_secret_key"

from routes.auth import *
from routes.finance import *
from routes.ai import *
from routes.report import *


if __name__ == "__main__":
    app.run(debug=True)