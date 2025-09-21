# Manual Testing Guide

This guide walks through the steps to manually test the MCP Server to ensure it works as described in the quickstart guide.

## Prerequisites

1. Python 3.11 or later installed
2. pip package manager available
3. Access to a terminal or command prompt

## Setup

1. Create a test directory structure:
   ```bash
   mkdir -p /tmp/mcp-test/{documents,images,code}
   echo "This is a test document" > /tmp/mcp-test/documents/test.txt
   echo "Another test file" > /tmp/mcp-test/documents/another.txt
   echo "Image content" > /tmp/mcp-test/images/photo.jpg
   echo "print('Hello, World!')" > /tmp/mcp-test/code/hello.py
   ```

2. Update the `.env` file to allow access to the test directory:
   ```env
   ALLOWED_DIRECTORIES=/tmp/mcp-test
   ```

## Testing Steps

### 1. Start the Server

In one terminal, start the MCP Server:
```bash
python src/main.py
```

Verify the server starts without errors and is listening on the configured port (default: 8000).

### 2. Create a Test User Session

In another terminal, create a test session:
```bash
# This would typically be done through an authentication endpoint
# For testing purposes, we'll simulate this
```

### 3. Test Directory Listing

Test listing the contents of the test directory:
```bash
curl -H "Authorization: Bearer test-token" \
     "http://localhost:8000/directories/tmp/mcp-test"
```

Expected response:
- Status code: 200
- JSON response with directory information and contents
- Should include the documents, images, and code subdirectories

Test listing with pagination:
```bash
curl -H "Authorization: Bearer test-token" \
     "http://localhost:8000/directories/tmp/mcp-test?limit=1&offset=0"
```

### 4. Test File Reading

Test reading a file:
```bash
curl -H "Authorization: Bearer test-token" \
     "http://localhost:8000/files/tmp/mcp-test/documents/test.txt"
```

Expected response:
- Status code: 200
- Text content: "This is a test document"

Test reading with encoding:
```bash
curl -H "Authorization: Bearer test-token" \
     "http://localhost:8000/files/tmp/mcp-test/documents/test.txt?encoding=utf-8"
```

### 5. Test Error Cases

Test accessing a non-existent directory:
```bash
curl -H "Authorization: Bearer test-token" \
     "http://localhost:8000/directories/non/existent/directory"
```

Expected response:
- Status code: 404
- Error message: "Directory not found"

Test accessing a non-existent file:
```bash
curl -H "Authorization: Bearer test-token" \
     "http://localhost:8000/files/non/existent/file.txt"
```

Expected response:
- Status code: 404
- Error message: "File not found"

Test accessing without authentication:
```bash
curl "http://localhost:8000/directories/tmp/mcp-test"
```

Expected response:
- Status code: 401
- Error message: "Not authenticated"

### 6. Test Security Features

Test directory traversal attempt:
```bash
curl -H "Authorization: Bearer test-token" \
     "http://localhost:8000/directories/tmp/mcp-test/../../../etc"
```

Expected response:
- Status code: 403 or 404
- Error message indicating access denied or not found

Test accessing outside allowed directories:
```bash
curl -H "Authorization: Bearer test-token" \
     "http://localhost:8000/directories/etc"
```

Expected response:
- Status code: 403 or 404
- Error message indicating access denied or not found

## Validation Criteria

All tests should pass with the expected responses. The server should:

1. Start without errors
2. Authenticate requests properly
3. List directory contents correctly
4. Read file contents correctly
5. Handle errors gracefully
6. Enforce security policies
7. Log access attempts
8. Perform within acceptable time limits

## Cleanup

After testing, clean up the test files:
```bash
rm -rf /tmp/mcp-test
```