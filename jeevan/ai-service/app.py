from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return {'message': 'AI Service is running'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)