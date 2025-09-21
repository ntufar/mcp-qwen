# Quickstart Guide: MCP Server for LLM File Browsing

## Prerequisites
- Python 3.11 or later
- pip package manager
- Virtual environment (recommended)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp-server
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
1. Create a configuration file `.env`:
   ```env
   # Server configuration
   HOST=localhost
   PORT=8000
   DEBUG=false
   
   # Security configuration
   SECRET_KEY=your-secret-key
   ALLOWED_DIRECTORIES=/path/to/allowed/directories
   ```

2. Set up access policies in `policies.json`:
   ```json
   [
     {
       "name": "llm-read-policy",
       "description": "Allow LLMs to read files in allowed directories",
       "resources": ["/path/to/allowed/*"],
       "principals": ["llm-*"],
       "actions": ["read", "list"],
       "conditions": {}
     }
   ]
   ```

## Running the Server
1. Start the server:
   ```bash
   python main.py
   ```

2. The server will be available at `http://localhost:8000`

## Basic Usage for LLMs

### List Directory Contents
```bash
curl -H "Authorization: Bearer <token>" \
     "http://localhost:8000/directories/path/to/directory"
```

### Read File Contents
```bash
curl -H "Authorization: Bearer <token>" \
     "http://localhost:8000/files/path/to/file.txt"
```

## Authentication
1. Obtain an access token by authenticating with the authentication provider
2. Include the token in the Authorization header for all requests:
   ```
   Authorization: Bearer <token>
   ```

## Security Notes
- Always use HTTPS in production
- Regularly rotate secret keys
- Monitor audit logs for suspicious activity
- Limit allowed directories to only what is necessary
- Use strong authentication mechanisms

## Troubleshooting
- If you receive 403 errors, check that your access policies allow the requested operations
- If you receive 404 errors, verify that the file or directory path exists
- Check the server logs for detailed error information