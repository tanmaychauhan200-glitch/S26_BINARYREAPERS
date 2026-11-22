from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class AlertResponse(BaseModel):
    id: str
    module_type: str
    study_area_id: str
    job_id: Optional[str] = None
    alert_type: str
    severity: str
    description: str
    confidence_score: float
    validation_status: str
    geometry: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
