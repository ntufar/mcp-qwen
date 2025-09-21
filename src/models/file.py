from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FileModel(BaseModel):
    id: str
    name: str
    path: str
    size: int
    type: str
    modified_at: datetime
    created_at: datetime
    permissions: str