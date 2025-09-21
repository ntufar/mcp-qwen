from pydantic import BaseModel
from typing import List, Union, Optional
from datetime import datetime
from src.models.file import FileModel

class DirectoryModel(BaseModel):
    id: str
    name: str
    path: str
    size: int
    modified_at: datetime
    created_at: datetime
    permissions: str
    contents: List[Union[FileModel, 'DirectoryModel']] = []