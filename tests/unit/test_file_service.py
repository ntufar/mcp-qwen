import pytest
import os
import tempfile
from datetime import datetime
from src.services.file_service import FileService
from src.models.file import FileModel

# Set up test directory within allowed paths
TEST_BASE_DIR = "mcp_test"

def setup_module(module):
    """Set up test directory before running tests"""
    # Create the test directory in /tmp
    test_dir = os.path.join("/tmp", TEST_BASE_DIR)
    os.makedirs(test_dir, exist_ok=True)

def teardown_module(module):
    """Clean up test directory after running tests"""
    test_dir = os.path.join("/tmp", TEST_BASE_DIR)
    if os.path.exists(test_dir):
        import shutil
        shutil.rmtree(test_dir)

def test_get_file_info():
    """Test getting file information"""
    # Create a test file
    test_file_path = os.path.join(TEST_BASE_DIR, "test_file.txt")
    full_path = os.path.join("/tmp", test_file_path)
    with open(full_path, 'w') as tmp_file:
        tmp_file.write("Test content")
    
    try:
        # Get file info
        file_info = FileService.get_file_info(test_file_path)
        
        # Verify the file info
        assert isinstance(file_info, FileModel)
        assert file_info.name == "test_file.txt"
        # Use the resolved path for comparison
        assert file_info.path == os.path.abspath(full_path)
        assert file_info.size == 12  # "Test content" is 12 bytes
        assert file_info.type == ".txt"
        assert isinstance(file_info.modified_at, datetime)
        assert isinstance(file_info.created_at, datetime)
        
    finally:
        # Clean up the test file
        if os.path.exists(full_path):
            os.unlink(full_path)

def test_file_exists():
    """Test checking if a file exists"""
    # Create a test file
    test_file_path = os.path.join(TEST_BASE_DIR, "exists_test.txt")
    full_path = os.path.join("/tmp", test_file_path)
    with open(full_path, 'w') as tmp_file:
        tmp_file.write("Test content")
    
    try:
        # Check if file exists
        assert FileService.file_exists(test_file_path) == True
        
        # Check if non-existent file exists
        assert FileService.file_exists("non/existent/file.txt") == False
        
    finally:
        # Clean up the test file
        if os.path.exists(full_path):
            os.unlink(full_path)

def test_file_exists_invalid_path():
    """Test checking if a file exists with an invalid path"""
    # Test with invalid path
    assert FileService.file_exists("") == False
    # Note: Testing with None would raise an exception, which is handled in the service