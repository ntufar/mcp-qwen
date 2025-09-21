#!/usr/bin/env python3
"""
Simple Token Generator for MCP Server

This script generates an authentication token for the MCP Server.
"""

import sys
import os
import json
from datetime import datetime, timedelta
import secrets

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_simple_token():
    """Create a simple authentication token"""
    # Generate a random token
    token = secrets.token_urlsafe(32)
    
    # Create token information
    token_info = {
        "principal": "llm-user",
        "token": token,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
        "scopes": ["read", "list"]
    }
    
    print("="*60)
    print("MCP SERVER AUTHENTICATION TOKEN")
    print("="*60)
    print(f"Principal: {token_info['principal']}")
    print(f"Token: {token_info['token']}")
    print(f"Created: {token_info['created_at']}")
    print(f"Expires: {token_info['expires_at']}")
    print(f"Scopes: {', '.join(token_info['scopes'])}")
    print("="*60)
    
    # Save to files
    with open(".mcp_token", "w") as f:
        f.write(token)
    
    with open(".mcp_token.json", "w") as f:
        json.dump(token_info, f, indent=2)
    
    print("\nToken saved to:")
    print("  - .mcp_token (token only)")
    print("  - .mcp_token.json (full token information)")
    
    print("\n" + "-"*60)
    print("USAGE INSTRUCTIONS:")
    print("-"*60)
    print("1. Set as environment variable:")
    print(f'   export MCP_TOKEN="{token}"')
    print("\n2. Use with curl:")
    print(f'   curl -H "Authorization: Bearer $MCP_TOKEN" \\')
    print(f'        "http://localhost:8000/directories/tmp"')
    print("\n3. Use in Python:")
    print("   import os")
    print("   token = os.getenv('MCP_TOKEN')")
    print("   headers = {'Authorization': f'Bearer {token}'}")
    print("-"*60)
    
    return token

if __name__ == "__main__":
    create_simple_token()
