import pytest
from datetime import datetime
from src.models.file import FileModel

def test_file_model_creation():
    """Test creating a FileModel instance"""
    file_model = FileModel(
        id="123",
        name="test.txt",
        path="/tmp/test.txt",
        size=1024,
        type=".txt",
        modified_at=datetime.now(),
        created_at=datetime.now(),
        permissions="-rw-r--r--"
    )
    
    assert file_model.id == "123"
    assert file_model.name == "test.txt"
    assert file_model.path == "/tmp/test.txt"
    assert file_model.size == 1024
    assert file_model.type == ".txt"
    assert file_model.permissions == "-rw-r--r--"

def test_file_model_validation():
    """Test FileModel validation"""
    # This test will pass if the model is created correctly
    # Pydantic will raise validation errors if the data is invalid
    with pytest.raises(Exception):
        FileModel(
            id="123",
            name="test.txt",
            path="/tmp/test.txt",
            size="invalid",  # Should be int
            type=".txt",
            modified_at=datetime.now(),
            created_at=datetime.now(),
            permissions="-rw-r--r--"
        )