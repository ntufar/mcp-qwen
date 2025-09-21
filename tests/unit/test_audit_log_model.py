import pytest
from datetime import datetime
from src.models.audit_log import AuditLogModel

def test_audit_log_model_creation():
    """Test creating an AuditLogModel instance"""
    audit_log = AuditLogModel(
        id="log1",
        timestamp=datetime.now(),
        principal="user1",
        resource="/tmp/test.txt",
        action="read",
        outcome="success",
        details="File read successfully",
        ip_address="192.168.1.1"
    )
    
    assert audit_log.id == "log1"
    assert audit_log.principal == "user1"
    assert audit_log.resource == "/tmp/test.txt"
    assert audit_log.action == "read"
    assert audit_log.outcome == "success"
    assert audit_log.details == "File read successfully"
    assert audit_log.ip_address == "192.168.1.1"

def test_audit_log_model_different_outcomes():
    """Test creating AuditLogModel instances with different outcomes"""
    # Success outcome
    success_log = AuditLogModel(
        id="log2",
        timestamp=datetime.now(),
        principal="user2",
        resource="/home/user2/documents",
        action="list",
        outcome="success",
        details="Directory listed successfully",
        ip_address="10.0.0.1"
    )
    
    assert success_log.outcome == "success"
    
    # Denied outcome
    denied_log = AuditLogModel(
        id="log3",
        timestamp=datetime.now(),
        principal="user3",
        resource="/etc/passwd",
        action="read",
        outcome="denied",
        details="Access denied by policy",
        ip_address="172.16.0.1"
    )
    
    assert denied_log.outcome == "denied"
    
    # Error outcome
    error_log = AuditLogModel(
        id="log4",
        timestamp=datetime.now(),
        principal="user4",
        resource="/nonexistent/file.txt",
        action="read",
        outcome="error",
        details="File not found",
        ip_address="192.168.0.100"
    )
    
    assert error_log.outcome == "error"