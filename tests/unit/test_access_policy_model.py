import pytest
from datetime import datetime
from src.models.access_policy import AccessPolicyModel

def test_access_policy_model_creation():
    """Test creating an AccessPolicyModel instance"""
    policy_model = AccessPolicyModel(
        id="policy1",
        name="test-policy",
        description="A test policy",
        resources=["/tmp/*"],
        principals=["user1", "user2"],
        actions=["read", "list"],
        conditions={"time": "business_hours"},
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    assert policy_model.id == "policy1"
    assert policy_model.name == "test-policy"
    assert policy_model.description == "A test policy"
    assert policy_model.resources == ["/tmp/*"]
    assert policy_model.principals == ["user1", "user2"]
    assert policy_model.actions == ["read", "list"]
    assert policy_model.conditions == {"time": "business_hours"}

def test_access_policy_model_empty_conditions():
    """Test creating an AccessPolicyModel with empty conditions"""
    policy_model = AccessPolicyModel(
        id="policy2",
        name="test-policy-2",
        description="Another test policy",
        resources=["/home/*"],
        principals=["admin"],
        actions=["read", "write", "delete"],
        conditions={},
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    assert policy_model.id == "policy2"
    assert policy_model.name == "test-policy-2"
    assert policy_model.conditions == {}