"""
MCP Server Client

This module provides a Python client for interacting with the MCP Server API.
It handles authentication, API calls, and response parsing.

Example usage:
    client = MCPServerClient("http://localhost:8000", "your-auth-token")
    directory_contents = client.list_directory("documents")
    file_contents = client.read_file("documents/example.txt")
"""

import requests
import json
from typing import Optional, Dict, List, Union

class MCPServerClient:
    """
    A client for interacting with the MCP Server API.
    
    Attributes:
        base_url (str): The base URL of the MCP Server (e.g., 'http://localhost:8000')
        token (str): The authentication token
        headers (dict): HTTP headers including the authorization token
    """
    
    def __init__(self, base_url: str, token: str):
        """
        Initialize the MCP Server client.
        
        Args:
            base_url (str): The base URL of the MCP Server
            token (str): The authentication token
        """
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def list_directory(self, path: str, recursive: bool = False, 
                      limit: int = 100, offset: int = 0) -> Optional[Dict]:
        """
        List the contents of a directory.
        
        Args:
            path (str): The path to the directory
            recursive (bool): Whether to list contents recursively
            limit (int): Maximum number of items to return (1-1000)
            offset (int): Number of items to skip
            
        Returns:
            dict: Directory information and contents, or None if request failed
            
        Example:
            >>> client = MCPServerClient("http://localhost:8000", "token")
            >>> result = client.list_directory("documents")
            >>> print(result["contents"])
        """
        # Construct the URL with query parameters
        url = f"{self.base_url}/directories/{path.lstrip('/')}"
        params = {
            "recursive": str(recursive).lower(),
            "limit": limit,
            "offset": offset
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error listing directory '{path}': {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response for directory '{path}': {e}")
            return None
    
    def read_file(self, path: str, encoding: str = "utf-8", 
                 limit: int = 10485760) -> Optional[str]:
        """
        Read the contents of a file.
        
        Args:
            path (str): The path to the file
            encoding (str): File encoding (default: utf-8)
            limit (int): Maximum number of bytes to read (default: 10MB)
            
        Returns:
            str: File contents as string, or None if request failed
            
        Example:
            >>> client = MCPServerClient("http://localhost:8000", "token")
            >>> content = client.read_file("documents/example.txt")
            >>> print(content)
        """
        # Construct the URL with query parameters
        url = f"{self.base_url}/files/{path.lstrip('/')}"
        params = {
            "encoding": encoding,
            "limit": limit
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error reading file '{path}': {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Initialize the client
    client = MCPServerClient("http://localhost:8000", "your-auth-token")
    
    # List directory contents
    print("Listing directory contents...")
    directory_info = client.list_directory("documents")
    if directory_info:
        print(f"Directory: {directory_info['name']}")
        print(f"Items: {directory_info['total_count']}")
        for item in directory_info['contents']:
            print(f"  - {item['name']} ({item['type']})")
    
    # Read a file
    print("\nReading file contents...")
    file_content = client.read_file("documents/example.txt")
    if file_content:
        print("File content:")
        print(file_content[:200] + "..." if len(file_content) > 200 else file_content)