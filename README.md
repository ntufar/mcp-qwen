# MCP Server for LLM File Browsing

The MCP Server is a security-focused server application that enables LLMs to safely browse and access local file systems. It provides a RESTful API with comprehensive authentication, authorization, and audit logging capabilities.

## Features

- **Secure File Access**: Strict access controls and sandboxing for all file operations
- **RESTful API**: Easy-to-use HTTP API for listing directories and reading files
- **Authentication**: OAuth2 Bearer token authentication
- **Authorization**: Attribute-based access control (ABAC) for fine-grained permissions
- **Audit Logging**: Comprehensive logging of all access attempts
- **Performance**: Optimized for low latency and high throughput
- **Cross-Platform**: Works on Linux, Windows, and macOS

## Prerequisites

- Python 3.11 or later
- pip package manager

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
   python src/main.py
   ```

2. The server will be available at `http://localhost:8000`

## Examples

The repository includes examples showing how to integrate with the MCP Server:

```bash
# Explore the examples directory
ls examples/

# Run the Python client example
python examples/mcp_client.py

# Run the Gemini integration example (requires API keys)
python examples/gemini_integration.py

# Run the curl examples
./examples/usage_examples.sh
```

See [examples/README.md](examples/README.md) for more details.

## API Usage

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

## Security

The MCP Server implements multiple layers of security:

1. **Authentication**: OAuth2 Bearer token authentication
2. **Authorization**: Attribute-based access control (ABAC)
3. **Audit Logging**: Comprehensive logging of all access attempts
4. **Input Validation**: Strict validation and sanitization of all inputs
5. **Path Security**: Secure path resolution to prevent directory traversal

For more details, see the [Security Documentation](docs/security.md).

## Documentation

- [API Documentation](docs/api.md)
- [Security Documentation](docs/security.md)
- [Examples](examples/README.md)

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite to ensure everything works
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue on the GitHub repository.