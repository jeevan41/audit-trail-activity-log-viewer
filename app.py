from flask import Flask
from flask_cors import CORS
from routes.describe_routes import describe_bp
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

@app.after_request
def add_security_headers(response):

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"

    return response

app.register_blueprint(describe_bp)

START_TIME = time.time()

@app.route("/")
def home():
    return {
        "message": "AI Service Running Successfully"
    }

@app.route("/health")
def health():

    uptime_seconds = int(time.time() - START_TIME)

    return {
        "status": "UP",
        "model": "Mock-AI-Model",
        "avg_response_time_ms": 120,
        "uptime_seconds": uptime_seconds,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)