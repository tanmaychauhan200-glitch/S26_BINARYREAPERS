from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import date, datetime

class SatelliteSceneBase(BaseModel):
    provider: str = "copernicus"
    satellite: str
    sensor: str
    product_id: str
    acquisition_date: date
    cloud_cover_pct: float
    processing_level: str = "LEVEL-2A"
    crs: str = "EPSG:4326"
    resolution_m: float = 10.0
    footprint: Dict[str, Any]
    download_status: str = "AVAILABLE"
    local_path: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None

class SatelliteSceneResponse(SatelliteSceneBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class SceneSearchRequest(BaseModel):
    module_type: Optional[str] = None
    study_area_id: Optional[str] = None
    bbox: Optional[List[float]] = None
    date_start: Optional[date] = None
    date_end: Optional[date] = None
    max_cloud_cover: float = 20.0
    provider: str = "copernicus"
