from flask import Flask
from flask_cors import CORS
from routes.describe_routes import describe_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(describe_bp)

@app.route("/")
def home():
    return {
        "message": "AI Service Running Successfully"
    }

@app.route("/health")
def health():
    return {
        "status": "UP"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)