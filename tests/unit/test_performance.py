import pytest
import time
import tempfile
import os
import shutil
from src.services.directory_service import DirectoryService
from src.services.file_service import FileService

# Set up test directory within allowed paths
TEST_BASE_DIR = "mcp_test"

def setup_module(module):
    """Set up test directory before running tests"""
    os.makedirs(os.path.join("/tmp", TEST_BASE_DIR), exist_ok=True)

def teardown_module(module):
    """Clean up test directory after running tests"""
    test_dir = os.path.join("/tmp", TEST_BASE_DIR)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

def test_directory_listing_performance():
    """Test that directory listing is fast"""
    # Create a test directory
    test_dir = os.path.join(TEST_BASE_DIR, "perf_test")
    full_path = os.path.join("/tmp", test_dir)
    os.makedirs(full_path, exist_ok=True)
    
    # Create some test files
    test_files = [f"file{i}.txt" for i in range(100)]  # 100 files
    for file_name in test_files:
        with open(os.path.join(full_path, file_name), "w") as f:
            f.write(f"Content of {file_name}")
    
    # Measure time to list directory contents
    start_time = time.time()
    contents = DirectoryService.list_directory_contents(test_dir, limit=100, offset=0)
    end_time = time.time()
    
    # Calculate duration
    duration = end_time - start_time
    
    # Assert that it's less than 100ms
    assert duration < 0.1, f"Directory listing took {duration:.3f}s, which is slower than 100ms"
    
    # Verify we got the right number of files
    assert len(contents) == 100

def test_file_info_performance():
    """Test that getting file info is fast"""
    # Create a test file
    test_file_path = os.path.join(TEST_BASE_DIR, "file_info_test.txt")
    full_path = os.path.join("/tmp", test_file_path)
    with open(full_path, 'w') as tmp_file:
        tmp_file.write("Test content")
    
    try:
        # Measure time to get file info
        start_time = time.time()
        file_info = FileService.get_file_info(test_file_path)
        end_time = time.time()
        
        # Calculate duration
        duration = end_time - start_time
        
        # Assert that it's less than 100ms
        assert duration < 0.1, f"Getting file info took {duration:.3f}s, which is slower than 100ms"
        
        # Verify we got file info
        assert file_info is not None
        assert file_info.size == 12  # "Test content" is 12 bytes
        
    finally:
        # Clean up the test file
        if os.path.exists(full_path):
            os.unlink(full_path)

def test_file_reading_performance():
    """Test that reading file content is fast"""
    # Create a test file with some content
    content = "A" * 10000  # 10KB of content
    test_file_path = os.path.join(TEST_BASE_DIR, "file_read_test.txt")
    full_path = os.path.join("/tmp", test_file_path)
    with open(full_path, 'w') as tmp_file:
        tmp_file.write(content)
    
    try:
        # Measure time to read file content
        start_time = time.time()
        file_content = FileService.read_file_content(test_file_path, limit=100000)
        end_time = time.time()
        
        # Calculate duration
        duration = end_time - start_time
        
        # Assert that it's less than 100ms
        assert duration < 0.1, f"Reading file content took {duration:.3f}s, which is slower than 100ms"
        
        # Verify we got the content
        assert file_content == content
        
    finally:
        # Clean up the test file
        if os.path.exists(full_path):
            os.unlink(full_path)