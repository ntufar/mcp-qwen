from pydantic import BaseModel
from datetime import datetime

class AuditLogModel(BaseModel):
    id: str
    timestamp: datetime
    principal: str
    resource: str
    action: str
    outcome: str
    details: str
    ip_address: str