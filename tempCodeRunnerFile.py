from flask import Flask
from routes.report import report_bp

app = Flask(__name__)
app.register_blueprint(report_bp)
# Secret Key
app.secret_key = "your_secret_key"

# Import all routes
from routes.auth import *
from routes.finance import *
from routes.ai import *
from routes.report import *


if __name__ == "__main__":
    app.run(debug=True)