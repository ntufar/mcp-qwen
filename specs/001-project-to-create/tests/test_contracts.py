# Contract Tests for File Browsing API

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_directory_success():
    """Test successful directory listing"""
    response = client.get("/directories/home/user/documents")
    assert response.status_code == 200
    data = response.json()
    assert "directory" in data
    assert "contents" in data
    assert isinstance(data["contents"], list)

def test_list_directory_not_found():
    """Test directory not found error"""
    response = client.get("/directories/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "Directory not found"

def test_list_directory_access_denied():
    """Test access denied error"""
    response = client.get("/directories/system")
    assert response.status_code == 403
    data = response.json()
    assert data["error"] == "Access denied"

def test_read_file_success():
    """Test successful file reading"""
    response = client.get("/files/home/user/documents/readme.txt")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"

def test_read_file_not_found():
    """Test file not found error"""
    response = client.get("/files/nonexistent.txt")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "File not found"

def test_read_file_access_denied():
    """Test access denied error"""
    response = client.get("/files/system/config.txt")
    assert response.status_code == 403
    data = response.json()
    assert data["error"] == "Access denied"

def test_read_large_file():
    """Test large file error"""
    response = client.get("/files/home/user/largefile.zip?limit=100000000")
    assert response.status_code == 413
    data = response.json()
    assert data["error"] == "File too large"