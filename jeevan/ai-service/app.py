from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from groq import Groq
import json
import redis
import hashlib
import time

app = Flask(__name__)
CORS(app)

# Track startup time for uptime
start_time = time.time()

# Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def load_prompt():
    with open('prompts/primary_prompt.txt', 'r') as f:
        return f.read()

def get_cache_key(text):
    return hashlib.sha256(text.encode()).hexdigest()

def get_cached_response(key):
    return redis_client.get(key)

def set_cached_response(key, response, ttl=900):
    redis_client.setex(key, ttl, json.dumps(response))

# Track response times
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';"
    return response

@app.route('/')
def hello():
    return {'message': 'AI Service is running'}

@app.route('/health', methods=['GET'])
def health():
    uptime = time.time() - start_time
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    return jsonify({
        'status': 'healthy',
        'model': 'mixtral-8x7b-32768',
        'avg_response_time': round(avg_response_time, 2),
        'uptime': round(uptime, 2)
    })

@app.route('/describe', methods=['POST'])
def describe():
    start = time.time()
    try:
        data = request.get_json()
        if not data or 'log_entry' not in data:
            return jsonify({'error': 'Missing log_entry in request body'}), 400
        
        log_entry = data['log_entry']
        if not isinstance(log_entry, str) or not log_entry.strip():
            return jsonify({'error': 'log_entry must be a non-empty string'}), 400
        
        cache_key = get_cache_key(f"describe:{log_entry}")
        cached = get_cached_response(cache_key)
        if cached:
            response_times.append(time.time() - start)
            return jsonify(json.loads(cached))
        
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
        
        result = {
            'description': generated_description,
            'generated_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        set_cached_response(cache_key, result)
        response_times.append(time.time() - start)
        return jsonify(result)
    
    except Exception as e:
        response_times.append(time.time() - start)
        return jsonify({'error': str(e)}), 500

@app.route('/recommend', methods=['POST'])
def recommend():
    start = time.time()
    try:
        data = request.get_json()
        if not data or 'log_entry' not in data:
            return jsonify({'error': 'Missing log_entry in request body'}), 400
        
        log_entry = data['log_entry']
        if not isinstance(log_entry, str) or not log_entry.strip():
            return jsonify({'error': 'log_entry must be a non-empty string'}), 400
        
        cache_key = get_cache_key(f"recommend:{log_entry}")
        cached = get_cached_response(cache_key)
        if cached:
            response_times.append(time.time() - start)
            return jsonify(json.loads(cached))
        
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
        
        result = {
            'recommendations': recommendations,
            'generated_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        set_cached_response(cache_key, result)
        response_times.append(time.time() - start)
        return jsonify(result)
    
    except json.JSONDecodeError:
        response_times.append(time.time() - start)
        return jsonify({'error': 'Failed to parse AI response as JSON'}), 500
    except Exception as e:
        response_times.append(time.time() - start)
        return jsonify({'error': str(e)}), 500

@app.route('/generate-report', methods=['POST'])
def generate_report():
    start = time.time()
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
        
        logs_text = '\n'.join(logs)
        cache_key = get_cache_key(f"report:{logs_text}")
        cached = get_cached_response(cache_key)
        if cached:
            response_times.append(time.time() - start)
            return jsonify(json.loads(cached))
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return jsonify({'error': 'GROQ_API_KEY environment variable not set'}), 500
        
        client = Groq(api_key=api_key)
        
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
        
        set_cached_response(cache_key, report)
        response_times.append(time.time() - start)
        return jsonify(report)
    
    except json.JSONDecodeError:
        response_times.append(time.time() - start)
        return jsonify({'error': 'Failed to parse AI response as JSON'}), 500
    except Exception as e:
        response_times.append(time.time() - start)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)