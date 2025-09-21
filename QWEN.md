# QWEN.md - MCP Server for LLM File Browsing

## Project Overview

This is the **MCP Server for LLM File Browsing**, a security-focused server application that enables Large Language Models (LLMs) to safely browse and access local file systems. The project provides a RESTful API with comprehensive authentication, authorization, and audit logging capabilities.

### Purpose
The primary purpose of this server is to allow LLMs to access file system information in a controlled, secure manner while preventing unauthorized access to sensitive files or directories.

### Main Technologies
- **Python 3.11+**: Primary programming language
- **FastAPI**: High-performance web framework for building the RESTful API
- **Pydantic**: Data validation and settings management using Python type hints
- **Uvicorn**: ASGI server for running the FastAPI application
- **OAuth2/JWT**: Authentication mechanism using Bearer tokens
- **Pytest**: Testing framework for unit, integration, and contract tests

### Architecture
The project follows a layered architecture with clear separation of concerns:

1. **API Layer** (`src/api/`)
   - RESTful endpoints for directory listing and file reading
   - Request/response handling and validation

2. **Service Layer** (`src/services/`)
   - Business logic implementation
   - File and directory operations
   - Authentication, access control, and audit services

3. **Model Layer** (`src/models/`)
   - Data models and structures
   - Pydantic models for request/response validation

4. **Middleware Layer** (`src/middleware/`)
   - Authentication, access control, and audit logging middleware
   - Cross-cutting concerns

5. **Utility Layer** (`src/utils/`)
   - Helper functions and utilities
   - Path validation, error handling, and caching

## Building and Running

### Prerequisites
- Python 3.11 or later
- pip package manager

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp-qwen
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

### Configuration
1. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file to configure:
   - Server settings (HOST, PORT, DEBUG)
   - Security settings (SECRET_KEY, ALLOWED_DIRECTORIES)

### Running the Server
Start the server in development mode:
```bash
python src/main.py
```

For production deployment, use:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Testing
Run the complete test suite:
```bash
python -m pytest tests/
```

Run tests with coverage:
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## Development Conventions

### Code Organization
The project follows a modular structure with clear separation of concerns:

- **Models** (`src/models/`): Data models and structures
- **Services** (`src/services/`): Business logic implementation
- **API** (`src/api/`): RESTful endpoints
- **Middleware** (`src/middleware/`): Cross-cutting concerns
- **Utilities** (`src/utils/`): Helper functions
- **Configuration** (`src/config.py`): Application configuration

### Coding Style
- Follow PEP 8 style guide
- Use Black for code formatting
- Use isort for import sorting
- Use type hints for all function signatures
- Write docstrings for all public functions and classes

### Testing Practices
- Follow Test-Driven Development (TDD) approach
- Write unit tests for all business logic
- Write integration tests for API endpoints
- Write contract tests to verify API behavior
- Maintain high test coverage (>90%)

### Git Workflow
- Use feature branches for new development
- Create pull requests for code review
- Squash commits before merging
- Follow conventional commit messages
- Update documentation with feature changes

### Security Considerations
- Validate all user inputs
- Sanitize file paths to prevent directory traversal
- Implement proper authentication and authorization
- Log all access attempts for audit purposes
- Use HTTPS in production deployments
- Regularly update dependencies

## Project Structure

```
.
├── docs/                    # Documentation files
│   ├── api.md              # API documentation
│   └── security.md         # Security implementation details
├── src/                    # Source code
│   ├── api/                # API endpoints
│   ├── middleware/         # Middleware components
│   ├── models/             # Data models
│   ├── services/           # Business logic services
│   ├── utils/              # Utility functions
│   ├── config.py           # Configuration management
│   └── main.py             # Application entry point
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── contract/           # Contract tests
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project configuration
├── .env.example           # Environment variables example
├── .gitignore             # Git ignore patterns
└── README.md              # Project documentation
```

## Key Components

### Core Services
1. **FileService** (`src/services/file_service.py`)
   - Reading file contents
   - Getting file information
   - Checking file existence

2. **DirectoryService** (`src/services/directory_service.py`)
   - Listing directory contents
   - Getting directory information
   - Checking directory existence

3. **AuthService** (`src/services/auth_service.py`)
   - User authentication
   - Token validation
   - Session management

4. **AccessControlService** (`src/services/access_control_service.py`)
   - Authorization checks
   - Policy enforcement
   - Permission validation

5. **AuditService** (`src/services/audit_service.py`)
   - Access logging
   - Audit trail management
   - Security event recording

### API Endpoints
1. **GET /directories/{path}** - List directory contents
   - Supports pagination
   - Returns file and directory metadata

2. **GET /files/{path}** - Read file contents
   - Supports encoding specification
   - Size limits for large files

### Security Features
1. **OAuth2 Bearer Token Authentication**
   - Token-based authentication
   - Secure session management

2. **Attribute-Based Access Control (ABAC)**
   - Fine-grained permissions
   - Policy-based authorization

3. **Audit Logging**
   - Comprehensive access logging
   - Security event tracking

4. **Path Validation**
   - Directory traversal prevention
   - Path sanitization
   - Allowed directory restrictions

## Usage Examples

### Starting the Server
```bash
# Development mode
python src/main.py

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using the API
```bash
# List directory contents
curl -H "Authorization: Bearer <token>" \
     "http://localhost:8000/directories/path/to/directory"

# Read file contents
curl -H "Authorization: Bearer <token>" \
     "http://localhost:8000/files/path/to/file.txt"
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test category
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/contract/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing
```

## Configuration Options

Environment variables that can be set in the `.env` file:

- `HOST`: Server hostname (default: localhost)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Debug mode (default: false)
- `SECRET_KEY`: Secret key for authentication
- `ALLOWED_DIRECTORIES`: Comma-separated list of allowed directories

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite to ensure everything works
6. Submit a pull request

Follow the established coding conventions and ensure all tests pass before submitting a pull request.