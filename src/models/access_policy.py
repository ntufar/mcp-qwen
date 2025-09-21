from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class AccessPolicyModel(BaseModel):
    id: str
    name: str
    description: str
    resources: List[str]
    principals: List[str]
    actions: List[str]
    conditions: Dict[str, Any]
    created_at: datetime
    updated_at: datetime