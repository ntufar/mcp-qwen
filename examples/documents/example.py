#!/usr/bin/env python3
"""
Example Python Script

This is an example Python script used for testing the MCP Server.
"""

import os
import sys
from datetime import datetime

def main():
    """Main function"""
    print("Example Python Script")
    print(f"Current time: {datetime.now()}")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    # List files in current directory
    files = os.listdir('.')
    print(f"Files in directory: {files}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())