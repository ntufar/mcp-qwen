#!/bin/bash

# MCP Server Usage Examples
# This script demonstrates how to interact with the MCP Server using curl commands

# Server configuration
MCP_SERVER="http://localhost:8000"
AUTH_TOKEN="your-auth-token-here"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== MCP Server Usage Examples ===${NC}"
echo ""

# Check if server is running
echo -e "${YELLOW}Checking if MCP Server is running...${NC}"
if curl -s -o /dev/null -w "%{http_code}" "$MCP_SERVER" | grep -q "200\|404\|401"; then
    echo -e "${GREEN}✓ MCP Server is accessible${NC}"
else
    echo -e "${RED}✗ MCP Server is not accessible. Please start the server first.${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}=== Authentication Examples ===${NC}"

# Example: Get directory listing with authentication
echo "1. Listing directory contents:"
echo "   curl -H \"Authorization: Bearer $AUTH_TOKEN\" \\"
echo "        \"$MCP_SERVER/directories/tmp\""
echo ""
echo "Response:"
curl -s -H "Authorization: Bearer $AUTH_TOKEN" \
     "$MCP_SERVER/directories/tmp" | jq '.' || echo "{}"
echo ""

# Example: Read file contents with authentication
echo "2. Reading file contents:"
echo "   curl -H \"Authorization: Bearer $AUTH_TOKEN\" \\"
echo "        \"$MCP_SERVER/files/tmp/example.txt\""
echo ""
echo "Response:"
curl -s -H "Authorization: Bearer $AUTH_TOKEN" \
     "$MCP_SERVER/files/tmp/example.txt" || echo "File content would appear here"
echo ""

echo ""
echo -e "${YELLOW}=== Query Parameter Examples ===${NC}"

# Example: List directory with pagination
echo "3. Listing directory with pagination (first 5 items):"
echo "   curl -H \"Authorization: Bearer $AUTH_TOKEN\" \\"
echo "        \"$MCP_SERVER/directories/tmp?limit=5&offset=0\""
echo ""

# Example: Read file with specific encoding
echo "4. Reading file with specific encoding:"
echo "   curl -H \"Authorization: Bearer $AUTH_TOKEN\" \\"
echo "        \"$MCP_SERVER/files/tmp/example.txt?encoding=utf-8\""
echo ""

# Example: Read file with size limit
echo "5. Reading file with size limit (1MB):"
echo "   curl -H \"Authorization: Bearer $AUTH_TOKEN\" \\"
echo "        \"$MCP_SERVER/files/tmp/largefile.txt?limit=1048576\""
echo ""

echo ""
echo -e "${YELLOW}=== Error Handling Examples ===${NC}"

# Example: Access denied (wrong token)
echo "6. Access denied (invalid token):"
echo "   curl -H \"Authorization: Bearer invalid-token\" \\"
echo "        \"$MCP_SERVER/directories/tmp\""
echo ""
echo "Response:"
curl -s -H "Authorization: Bearer invalid-token" \
     "$MCP_SERVER/directories/tmp" | jq '.' || echo "{}"
echo ""

# Example: File not found
echo "7. File not found:"
echo "   curl -H \"Authorization: Bearer $AUTH_TOKEN\" \\"
echo "        \"$MCP_SERVER/files/tmp/nonexistent.txt\""
echo ""
echo "Response:"
curl -s -H "Authorization: Bearer $AUTH_TOKEN" \
     "$MCP_SERVER/files/tmp/nonexistent.txt" | jq '.' || echo "{}"
echo ""

echo ""
echo -e "${YELLOW}=== Python Client Usage ===${NC}"
echo "To use the Python client, run:"
echo "   python examples/mcp_client.py"
echo ""

echo -e "${YELLOW}=== Gemini Integration ===${NC}"
echo "To use with Gemini, first set your API keys:"
echo "   export GEMINI_API_KEY='your-gemini-api-key'"
echo "   export MCP_TOKEN='your-mcp-auth-token'"
echo ""
echo "Then run:"
echo "   python examples/gemini_integration.py"
echo ""

echo -e "${GREEN}=== End of Examples ===${NC}"