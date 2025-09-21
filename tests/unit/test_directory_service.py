import pytest
import os
import tempfile
from src.services.directory_service import DirectoryService
from src.models.directory import DirectoryModel

# Set up test directory within allowed paths
TEST_BASE_DIR = "mcp_test"

def setup_module(module):
    """Set up test directory before running tests"""
    os.makedirs(os.path.join("/tmp", TEST_BASE_DIR), exist_ok=True)

def teardown_module(module):
    """Clean up test directory after running tests"""
    test_dir = os.path.join("/tmp", TEST_BASE_DIR)
    if os.path.exists(test_dir):
        import shutil
        shutil.rmtree(test_dir)

def test_get_directory_info():
    """Test getting directory information"""
    # Create a test directory
    test_dir = os.path.join(TEST_BASE_DIR, "test_dir")
    full_path = os.path.join("/tmp", test_dir)
    os.makedirs(full_path, exist_ok=True)
    
    # Get directory info
    dir_info = DirectoryService.get_directory_info(test_dir)
    
    # Verify the directory info
    assert isinstance(dir_info, DirectoryModel)
    assert dir_info.name == "test_dir"
    assert dir_info.path == os.path.abspath(full_path)
    assert isinstance(dir_info.size, int)
    assert dir_info.permissions.startswith("d")  # Directory permissions start with "d"

def test_directory_exists():
    """Test checking if a directory exists"""
    # Create a test directory
    test_dir = os.path.join(TEST_BASE_DIR, "exists_test")
    full_path = os.path.join("/tmp", test_dir)
    os.makedirs(full_path, exist_ok=True)
    
    # Check if directory exists
    assert DirectoryService.directory_exists(test_dir) == True
    
    # Check if non-existent directory exists
    assert DirectoryService.directory_exists("non/existent/directory") == False

def test_list_directory_contents():
    """Test listing directory contents"""
    # Create a test directory
    test_dir = os.path.join(TEST_BASE_DIR, "list_test")
    full_path = os.path.join("/tmp", test_dir)
    os.makedirs(full_path, exist_ok=True)
    
    # Create some test files
    test_files = ["file1.txt", "file2.txt", "file3.txt"]
    for file_name in test_files:
        with open(os.path.join(full_path, file_name), "w") as f:
            f.write(f"Content of {file_name}")
    
    # List directory contents
    contents = DirectoryService.list_directory_contents(test_dir, limit=10, offset=0)
    
    # Verify the contents
    assert len(contents) == 3
    # Note: The actual content types might vary depending on the system

def test_list_directory_contents_pagination():
    """Test listing directory contents with pagination"""
    # Create a test directory
    test_dir = os.path.join(TEST_BASE_DIR, "pagination_test")
    full_path = os.path.join("/tmp", test_dir)
    os.makedirs(full_path, exist_ok=True)
    
    # Create some test files
    test_files = [f"file{i}.txt" for i in range(1, 11)]  # 10 files
    for file_name in test_files:
        with open(os.path.join(full_path, file_name), "w") as f:
            f.write(f"Content of {file_name}")
    
    # List directory contents with limit
    contents = DirectoryService.list_directory_contents(test_dir, limit=5, offset=0)
    
    # Verify the contents
    assert len(contents) == 5
    
    # List next page
    contents_page_2 = DirectoryService.list_directory_contents(test_dir, limit=5, offset=5)
    
    # Verify the contents
    assert len(contents_page_2) == 5