from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

class StudyAreaBase(BaseModel):
    name: str
    description: Optional[str] = None
    module_type: str
    state: str
    geometry: Dict[str, Any]
    area_ha: float = 0.0

class StudyAreaCreate(StudyAreaBase):
    pass

class StudyAreaResponse(StudyAreaBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
