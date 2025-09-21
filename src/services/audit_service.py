import json
import logging
from typing import Dict, Any, List
from src.models.audit_log import AuditLogModel
from datetime import datetime
import os

class AuditService:
    def __init__(self, log_file: str = "audit.log"):
        self.log_file = log_file
        # Set up logging
        self.logger = logging.getLogger("audit")
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(handler)
    
    def log_access(self, principal: str, resource: str, action: str, outcome: str, 
                   details: str = "", ip_address: str = "") -> AuditLogModel:
        """
        Log an access attempt.
        
        Args:
            principal: User or system making the request
            resource: Resource being accessed
            action: Action being performed
            outcome: Result of the action (success, denied, error)
            details: Additional details about the action
            ip_address: IP address of the requester
            
        Returns:
            AuditLogModel with the log entry
        """
        audit_log = AuditLogModel(
            id=str(hash(f"{principal}{resource}{action}{datetime.now()}")),
            timestamp=datetime.now(),
            principal=principal,
            resource=resource,
            action=action,
            outcome=outcome,
            details=details,
            ip_address=ip_address
        )
        
        # Log to file
        log_entry = {
            "id": audit_log.id,
            "timestamp": audit_log.timestamp.isoformat(),
            "principal": audit_log.principal,
            "resource": audit_log.resource,
            "action": audit_log.action,
            "outcome": audit_log.outcome,
            "details": audit_log.details,
            "ip_address": audit_log.ip_address
        }
        
        self.logger.info(json.dumps(log_entry))
        
        return audit_log
    
    def get_logs(self, limit: int = 100) -> List[AuditLogModel]:
        """
        Get recent audit logs.
        
        Args:
            limit: Maximum number of logs to return
            
        Returns:
            List of AuditLogModel objects
        """
        # In a real implementation, this would read from the log file
        # or a database and return parsed logs
        return []