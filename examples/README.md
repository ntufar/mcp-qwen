# MCP Server Examples

This directory contains example code showing how to integrate with the MCP Server from LLM applications.

## Files

1. `mcp_client.py` - Python client for the MCP Server
2. `gemini_integration.py` - Example integration with Google's Gemini
3. `policies.json` - Sample access policies configuration
4. `usage_examples.sh` - Shell script with curl examples

## Usage

These examples demonstrate how to:
- Authenticate with the MCP Server
- List directory contents
- Read file contents
- Integrate with LLM applications like Google's Gemini

## Getting Started

1. Make sure the MCP Server is running:
   ```bash
   cd ..
   python src/main.py
   ```

2. Set up your authentication token in the examples:
   ```bash
   export MCP_TOKEN="your-auth-token-here"
   ```

3. For Gemini integration, also set your Gemini API key:
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```

4. Run the examples:
   ```bash
   # Run the Python client example
   python mcp_client.py
   
   # Run the Gemini integration example
   python gemini_integration.py
   
   # Run the curl examples
   ./usage_examples.sh
   ```

## Security Notes

- Never commit authentication tokens or API keys to version control
- Use environment variables or secure configuration files
- Follow the principle of least privilege when configuring access policies
- Monitor audit logs for suspicious activity