import pytest
from datetime import datetime
from src.models.directory import DirectoryModel
from src.models.file import FileModel

def test_directory_model_creation():
    """Test creating a DirectoryModel instance"""
    # Create a file model for the contents
    file_model = FileModel(
        id="456",
        name="test.txt",
        path="/tmp/test/test.txt",
        size=512,
        type=".txt",
        modified_at=datetime.now(),
        created_at=datetime.now(),
        permissions="-rw-r--r--"
    )
    
    directory_model = DirectoryModel(
        id="123",
        name="test",
        path="/tmp/test",
        size=2048,
        modified_at=datetime.now(),
        created_at=datetime.now(),
        permissions="drwxr-xr-x",
        contents=[file_model]
    )
    
    assert directory_model.id == "123"
    assert directory_model.name == "test"
    assert directory_model.path == "/tmp/test"
    assert directory_model.size == 2048
    assert directory_model.permissions == "drwxr-xr-x"
    assert len(directory_model.contents) == 1
    assert isinstance(directory_model.contents[0], FileModel)

def test_directory_model_empty_contents():
    """Test creating a DirectoryModel with empty contents"""
    directory_model = DirectoryModel(
        id="123",
        name="empty",
        path="/tmp/empty",
        size=4096,
        modified_at=datetime.now(),
        created_at=datetime.now(),
        permissions="drwxr-xr-x"
    )
    
    assert directory_model.id == "123"
    assert directory_model.name == "empty"
    assert directory_model.path == "/tmp/empty"
    assert directory_model.size == 4096
    assert directory_model.permissions == "drwxr-xr-x"
    assert len(directory_model.contents) == 0