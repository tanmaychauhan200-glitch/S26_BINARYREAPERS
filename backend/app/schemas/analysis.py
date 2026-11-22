from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

class AnalysisJobCreate(BaseModel):
    module_type: str
    study_area_id: str
    scene_before_id: Optional[str] = None
    scene_after_id: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class AnalysisJobResponse(BaseModel):
    id: str
    module_type: str
    study_area_id: str
    scene_before_id: Optional[str] = None
    scene_after_id: Optional[str] = None
    status: str
    progress_pct: float
    parameters_json: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AnalysisResultResponse(BaseModel):
    id: str
    job_id: str
    result_type: str
    raster_path: Optional[str] = None
    vector_geojson_path: Optional[str] = None
    total_change_ha: float
    summary_metrics: Optional[Dict[str, Any]] = None
    quality_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
