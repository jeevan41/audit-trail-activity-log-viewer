from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from groq import Groq
import json

app = Flask(__name__)
CORS(app)

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

@app.route('/recommend', methods=['POST'])
def recommend():
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
        full_prompt = f"{prompt}\n\nLog Entry: {log_entry}\n\nPlease provide exactly 3 recommendations for handling this log entry. Return them as a JSON array of objects, each with 'action_type', 'description', and 'priority' (high, medium, or low). Do not include any other text."
        
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": full_prompt}],
            max_tokens=500
        )
        
        generated_text = response.choices[0].message.content.strip()
        
        recommendations = json.loads(generated_text)
        
        if not isinstance(recommendations, list) or len(recommendations) != 3:
            return jsonify({'error': 'Invalid response format from AI'}), 500
        
        for rec in recommendations:
            if not all(k in rec for k in ['action_type', 'description', 'priority']):
                return jsonify({'error': 'Invalid recommendation structure'}), 500
        
        return jsonify({
            'recommendations': recommendations,
            'generated_at': datetime.utcnow().isoformat() + 'Z'
        })
    
    except json.JSONDecodeError:
        return jsonify({'error': 'Failed to parse AI response as JSON'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.get_json()
        if not data or 'logs' not in data:
            return jsonify({'error': 'Missing logs in request body'}), 400
        
        logs = data['logs']
        if not isinstance(logs, list) or not logs:
            return jsonify({'error': 'logs must be a non-empty array of strings'}), 400
        
        for log in logs:
            if not isinstance(log, str) or not log.strip():
                return jsonify({'error': 'All logs must be non-empty strings'}), 400
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return jsonify({'error': 'GROQ_API_KEY environment variable not set'}), 500
        
        client = Groq(api_key=api_key)
        
        logs_text = '\n'.join(f'- {log}' for log in logs)
        full_prompt = f"{load_prompt()}\n\nAudit Logs:\n{logs_text}\n\nGenerate a comprehensive audit report with the following structure:\n- title: A concise title for the report\n- summary: A brief overall summary\n- overview: Detailed overview of the audit period\n- key_items: Array of key findings or items\n- recommendations: Array of actionable recommendations\n\nReturn the response as a valid JSON object with these exact keys."
        
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": full_prompt}],
            max_tokens=1000
        )
        
        generated_text = response.choices[0].message.content.strip()
        
        # Try to parse as JSON
        report = json.loads(generated_text)
        
        required_keys = ['title', 'summary', 'overview', 'key_items', 'recommendations']
        if not all(k in report for k in required_keys):
            return jsonify({'error': 'Invalid report structure'}), 500
        
        report['generated_at'] = datetime.utcnow().isoformat() + 'Z'
        
        return jsonify(report)
    
    except json.JSONDecodeError:
        return jsonify({'error': 'Failed to parse AI response as JSON'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)