from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class UserSessionModel(BaseModel):
    id: str
    token: str
    principal: str
    created_at: datetime
    expires_at: datetime
    scopes: List[str]
    metadata: Dict[str, Any]