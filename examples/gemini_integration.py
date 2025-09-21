"""
Gemini Integration Example

This script demonstrates how to integrate the MCP Server with Google's Gemini AI model.
It shows how to use the MCP client to fetch file system information and incorporate
it into Gemini prompts.

Requirements:
- google-generativeai package
- MCP Server running
- Valid Gemini API key
- Valid MCP Server authentication token

Installation:
pip install google-generativeai
"""

import google.generativeai as genai
import os
from typing import Optional, Dict, Any
from examples.mcp_client import MCPServerClient

class GeminiMCPIntegration:
    """
    Integration class for using MCP Server with Google's Gemini AI.
    
    This class demonstrates how to:
    1. Fetch file system information from MCP Server
    2. Incorporate that information into Gemini prompts
    3. Generate responses based on file system context
    """
    
    def __init__(self, gemini_api_key: str, mcp_base_url: str, mcp_token: str):
        """
        Initialize the Gemini-MCP integration.
        
        Args:
            gemini_api_key (str): Your Gemini API key
            mcp_base_url (str): Base URL of the MCP Server
            mcp_token (str): Authentication token for MCP Server
        """
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Initialize MCP client
        self.mcp_client = MCPServerClient(mcp_base_url, mcp_token)
    
    def get_file_system_context(self, directory_path: str) -> Optional[str]:
        """
        Get file system context from MCP Server.
        
        Args:
            directory_path (str): Path to the directory to analyze
            
        Returns:
            str: Formatted string with directory contents, or None if failed
        """
        # Get directory listing
        directory_info = self.mcp_client.list_directory(directory_path)
        if not directory_info:
            return None
        
        # Format the directory information
        context_lines = [
            f"Directory: {directory_info['name']}",
            f"Path: {directory_info['path']}",
            f"Items ({directory_info['total_count']} total):"
        ]
        
        # Add information about each item
        for item in directory_info['contents']:
            if item['type'] == 'file':
                context_lines.append(f"  📄 {item['name']} ({item['size']} bytes)")
            elif item['type'] == 'directory':
                context_lines.append(f"  📁 {item['name']}/")
        
        return "\n".join(context_lines)
    
    def read_file_content(self, file_path: str) -> Optional[str]:
        """
        Read file content from MCP Server.
        
        Args:
            file_path (str): Path to the file to read
            
        Returns:
            str: File content, or None if failed
        """
        return self.mcp_client.read_file(file_path)
    
    def analyze_directory(self, directory_path: str, query: str) -> str:
        """
        Analyze a directory using Gemini and file system context.
        
        Args:
            directory_path (str): Path to the directory to analyze
            query (str): Question or instruction for Gemini
            
        Returns:
            str: Gemini's response based on the file system context
        """
        # Get file system context
        fs_context = self.get_file_system_context(directory_path)
        if not fs_context:
            return "Failed to retrieve file system context."
        
        # Create prompt with context
        prompt = f"""
        I have access to a directory on a file system. Here's what's in it:
        
        {fs_context}
        
        Based on this information, please answer the following question:
        
        {query}
        
        Provide a clear and concise response.
        """
        
        # Generate response using Gemini
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"
    
    def analyze_file(self, file_path: str, query: str) -> str:
        """
        Analyze a file's content using Gemini.
        
        Args:
            file_path (str): Path to the file to analyze
            query (str): Question or instruction for Gemini
            
        Returns:
            str: Gemini's response based on the file content
        """
        # Read file content
        file_content = self.read_file_content(file_path)
        if not file_content:
            return "Failed to read file content."
        
        # Truncate content if too long (Gemini has token limits)
        max_chars = 10000
        if len(file_content) > max_chars:
            file_content = file_content[:max_chars] + "\n... (content truncated)"
        
        # Create prompt with file content
        prompt = f"""
        I have access to a file with the following content:
        
        ```
        {file_content}
        ```
        
        Based on this content, please answer the following question:
        
        {query}
        
        Provide a clear and concise response.
        """
        
        # Generate response using Gemini
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"

# Example usage
if __name__ == "__main__":
    # Get API keys from environment variables (recommended)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")
    MCP_TOKEN = os.getenv("MCP_TOKEN", "your-mcp-auth-token")
    
    # Initialize the integration
    integration = GeminiMCPIntegration(
        gemini_api_key=GEMINI_API_KEY,
        mcp_base_url="http://localhost:8000",
        mcp_token=MCP_TOKEN
    )
    
    # Example 1: Analyze directory contents
    print("=== Analyzing Directory ===")
    result = integration.analyze_directory(
        directory_path="documents",
        query="What types of documents do I have? Are there any Python files?"
    )
    print(result)
    
    # Example 2: Analyze file content
    print("\n=== Analyzing File ===")
    result = integration.analyze_file(
        file_path="documents/example.py",
        query="What does this Python script do? Summarize its main functionality."
    )
    print(result)
    
    # Example 3: Find specific information
    print("\n=== Finding Information ===")
    result = integration.analyze_directory(
        directory_path="projects",
        query="Which project seems to be the most recently modified?"
    )
    print(result)