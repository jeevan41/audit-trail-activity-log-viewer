# AI Service

A Flask-based AI service for audit trail analysis using Groq's Mixtral model. Provides endpoints for describing log entries, generating recommendations, and creating audit reports.

## Features

- **Log Description**: Analyze individual audit log entries
- **Recommendations**: Generate actionable recommendations for log entries
- **Report Generation**: Create comprehensive audit reports from multiple logs
- **Health Monitoring**: Check service status and performance metrics
- **Redis Caching**: SHA256-keyed caching with 15-minute TTL
- **Security Headers**: OWASP-compliant security headers
- **Fallback Handling**: Graceful degradation on AI service failures

## Setup

### Prerequisites

- Python 3.8+
- Redis server
- Groq API key

### Installation

1. Clone the repository and navigate to the ai-service directory:
   ```bash
   cd ai-service
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start Redis server (if not already running):
   ```bash
   redis-server
   ```

## Environment Variables

Set the following environment variables:

- `GROQ_API_KEY`: Your Groq API key (required)

Example:
```bash
export GROQ_API_KEY=your_groq_api_key_here
```

## Running the Service

Start the Flask development server:
```bash
python app.py
```

The service will run on `http://localhost:5000`

## API Reference

### Health Check

**GET /health**

Returns service health status and metrics.

**Response:**
```json
{
  "status": "healthy",
  "model": "mixtral-8x7b-32768",
  "avg_response_time": 1.23,
  "uptime": 3600.5
}
```

### Describe Log Entry

**POST /describe**

Analyzes a single audit log entry and provides a detailed description.

**Request Body:**
```json
{
  "log_entry": "2023-10-01 10:00:00 - User 'john_doe' logged into system from IP 192.168.1.1"
}
```

**Response:**
```json
{
  "description": "User login event from IP 192.168.1.1. The login appears normal with no security concerns.",
  "generated_at": "2023-10-01T10:00:00.000Z"
}
```

**Error Response (Fallback):**
```json
{
  "description": "Unable to analyze log entry at this time. Please try again later.",
  "generated_at": "2023-10-01T10:00:00.000Z",
  "is_fallback": true
}
```

### Generate Recommendations

**POST /recommend**

Provides 3 recommendations for handling a log entry.

**Request Body:**
```json
{
  "log_entry": "2023-10-01 10:05:00 - Failed login attempt for user 'hacker' from IP 10.0.0.5"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "action_type": "alert",
      "description": "Send immediate alert to security team",
      "priority": "high"
    },
    {
      "action_type": "block",
      "description": "Block the IP address 10.0.0.5",
      "priority": "high"
    },
    {
      "action_type": "monitor",
      "description": "Increase monitoring for similar attempts",
      "priority": "medium"
    }
  ],
  "generated_at": "2023-10-01T10:05:00.000Z"
}
```

**Error Response (Fallback):**
```json
{
  "recommendations": [
    {
      "action_type": "monitor",
      "description": "Monitor the log entry for unusual activity",
      "priority": "medium"
    },
    {
      "action_type": "log",
      "description": "Ensure the event is properly logged",
      "priority": "low"
    },
    {
      "action_type": "review",
      "description": "Review similar entries for patterns",
      "priority": "low"
    }
  ],
  "generated_at": "2023-10-01T10:05:00.000Z",
  "is_fallback": true
}
```

### Generate Audit Report

**POST /generate-report**

Creates a comprehensive audit report from multiple log entries.

**Request Body:**
```json
{
  "logs": [
    "2023-10-01 10:00:00 - User 'john_doe' logged into system",
    "2023-10-01 10:05:00 - File accessed: /sensitive/data.txt",
    "2023-10-01 10:10:00 - Database query executed"
  ]
}
```

**Response:**
```json
{
  "title": "Weekly Audit Report - October 1-7, 2023",
  "summary": "Normal system activity with routine user logins and file accesses",
  "overview": "During the reporting period, the system experienced typical usage patterns...",
  "key_items": [
    "5 user logins",
    "3 file accesses",
    "2 database queries"
  ],
  "recommendations": [
    "Continue monitoring access patterns",
    "Review user permissions quarterly"
  ],
  "generated_at": "2023-10-01T10:15:00.000Z"
}
```

**Error Response (Fallback):**
```json
{
  "title": "Audit Report - Service Unavailable",
  "summary": "Unable to generate detailed report at this time.",
  "overview": "Please try again later.",
  "key_items": ["Service temporarily unavailable"],
  "recommendations": ["Retry the request", "Check system status"],
  "generated_at": "2023-10-01T10:15:00.000Z",
  "is_fallback": true
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input)
- `500`: Internal Server Error (AI service failure, includes fallback response)

## Caching

Responses are cached in Redis for 15 minutes using SHA256 hashes of the input data to improve performance and reduce API costs.

## Security

The service includes comprehensive security headers:
- Content Security Policy (CSP)
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Strict-Transport-Security
- Referrer-Policy
- Permissions-Policy

## Development

For development, ensure Redis is running and environment variables are set. The service uses Flask's debug mode for development.

## Production Deployment

For production:
1. Use a production WSGI server (gunicorn, uwsgi)
2. Set up proper environment variable management
3. Configure Redis cluster for scalability
4. Enable HTTPS
5. Set up monitoring and logging