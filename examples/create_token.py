#!/usr/bin/env python3
"""
Token Generator for MCP Server

This script generates an authentication token for the MCP Server.
"""

import sys
import os
import json

# Add src to path so we can import the services
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.auth_service import AuthService
from src.models.user_session import UserSessionModel

def main():
    """Main function to create a token"""
    try:
        print("Creating authentication token for MCP Server...")
        
        # Initialize the auth service
        auth_service = AuthService()
        
        # Create a session for an LLM user
        user_session = auth_service.create_session(
            principal="llm-user",
            scopes=["read", "list"],
            duration_hours=24  # Valid for 24 hours
        )
        
        print("\n" + "="*50)
        print("TOKEN GENERATED SUCCESSFULLY")
        print("="*50)
        print(f"Principal: {user_session.principal}")
        print(f"Token: {user_session.token}")
        print(f"Expires at: {user_session.expires_at}")
        print(f"Scopes: {', '.join(user_session.scopes)}")
        print("="*50)
        
        # Save to a file for easy access
        token_file = ".mcp_token"
        with open(token_file, "w") as f:
            f.write(user_session.token)
        
        print(f"\nToken saved to '{token_file}' file")
        
        # Also save as JSON for more detailed information
        token_info = {
            "principal": user_session.principal,
            "token": user_session.token,
            "expires_at": user_session.expires_at.isoformat(),
            "scopes": user_session.scopes,
            "created_at": user_session.created_at.isoformat()
        }
        
        with open(".mcp_token.json", "w") as f:
            json.dump(token_info, f, indent=2)
        
        print(f"Token info saved to '.mcp_token.json'")
        
        print("\n" + "-"*50)
        print("USAGE EXAMPLES:")
        print("-"*50)
        print("1. Set as environment variable:")
        print(f'   export MCP_TOKEN="{user_session.token}"')
        print("\n2. Use with curl:")
        print(f'   curl -H "Authorization: Bearer $MCP_TOKEN" \\')
        print(f'        "http://localhost:8000/directories/tmp"')
        print("\n3. Use in Python:")
        print("   import os")
        print("   token = os.getenv('MCP_TOKEN')")
        print("   headers = {'Authorization': f'Bearer {token}'}")
        print("-"*50)
        
        return 0
        
    except Exception as e:
        print(f"Error creating token: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
