from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from groq import Groq

app = Flask(__name__)
CORS(app)

# Groq client will be initialized when needed
# client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def load_prompt():
    with open('prompts/primary_prompt.txt', 'r') as f:
        return f.read()

@app.route('/')
def hello():
    return {'message': 'AI Service is running'}

@app.route('/describe', methods=['POST'])
def describe():
    try:
        data = request.get_json()
        if not data or 'log_entry' not in data:
            return jsonify({'error': 'Missing log_entry in request body'}), 400
        
        log_entry = data['log_entry']
        if not isinstance(log_entry, str) or not log_entry.strip():
            return jsonify({'error': 'log_entry must be a non-empty string'}), 400
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return jsonify({'error': 'GROQ_API_KEY environment variable not set'}), 500
        
        client = Groq(api_key=api_key)
        
        prompt = load_prompt()
        full_prompt = f"{prompt}\n\nLog Entry: {log_entry}\n\nPlease analyze the above log entry:"
        
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": full_prompt}],
            max_tokens=500
        )
        
        generated_description = response.choices[0].message.content.strip()
        
        return jsonify({
            'description': generated_description,
            'generated_at': datetime.utcnow().isoformat() + 'Z'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)