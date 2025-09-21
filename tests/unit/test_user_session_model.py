import pytest
from datetime import datetime, timedelta
from src.models.user_session import UserSessionModel

def test_user_session_model_creation():
    """Test creating a UserSessionModel instance"""
    session = UserSessionModel(
        id="session1",
        token="abc123xyz",
        principal="user1",
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(hours=1),
        scopes=["read", "list"],
        metadata={"department": "engineering", "role": "developer"}
    )
    
    assert session.id == "session1"
    assert session.token == "abc123xyz"
    assert session.principal == "user1"
    assert session.scopes == ["read", "list"]
    assert session.metadata == {"department": "engineering", "role": "developer"}

def test_user_session_model_empty_metadata():
    """Test creating a UserSessionModel with empty metadata"""
    session = UserSessionModel(
        id="session2",
        token="def456uvw",
        principal="user2",
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(hours=24),
        scopes=["read", "write", "delete"],
        metadata={}
    )
    
    assert session.id == "session2"
    assert session.token == "def456uvw"
    assert session.metadata == {}