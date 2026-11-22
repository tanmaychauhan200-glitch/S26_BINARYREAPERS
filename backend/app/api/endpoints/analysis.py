import requests
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from backend.app.geospatial.point_analyst import inspect_point_in_india
from backend.app.services.ai_analyst import ai_analyst

router = APIRouter()

class PointInspectRequest(BaseModel):
    latitude: float
    longitude: float

class AIAnalysisRequest(BaseModel):
    module_type: str = "riverwatch"
    area_name: str = "Target Location"
    latitude: float = 28.5
    longitude: float = 77.2
    spectral_metrics: Optional[Dict[str, Any]] = None
    total_change_ha: float = 18.4

@router.post("/point-inspect")
def inspect_point(payload: PointInspectRequest):
    """
    Analyzes any clicked or zoomed point across India.
    Returns reverse geocoding, UTM zone, land cover, and spectral indices.
    """
    if not (6.0 <= payload.latitude <= 38.0 and 68.0 <= payload.longitude <= 98.0):
        # Allow inspect even slightly outside Indian bounding box with fallback
        pass
    result = inspect_point_in_india(payload.latitude, payload.longitude)
    return result

@router.post("/ai-analyze")
def run_ai_analysis(payload: AIAnalysisRequest):
    """
    Invokes the AI Earth Observation Analyst (TerraWatch Ecological Intelligence Core / Gemini)
    to generate deep multi-spectral diagnostics and field inspection protocols.
    """
    report = ai_analyst.analyze_environmental_change(
        module_type=payload.module_type,
        area_name=payload.area_name,
        coordinates={"latitude": payload.latitude, "longitude": payload.longitude},
        spectral_metrics=payload.spectral_metrics or {"ndwi": 0.12, "ndvi": 0.28, "dndvi": 0.22},
        total_change_ha=payload.total_change_ha
    )
    return report

@router.get("/search-location")
def search_location(q: str = Query(..., min_length=2, description="City, river, forest, or landmark in India")):
    """
    Searches any place in India and returns coordinates and bounding boxes to fly to.
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "TerraWatch-360-India-Search/1.0"}
        params = {
            "q": q,
            "format": "json",
            "countrycodes": "in",
            "limit": 5
        }
        resp = requests.get(url, headers=headers, params=params, timeout=4.0)
        if resp.status_code == 200:
            results = []
            for item in resp.json():
                results.append({
                    "display_name": item.get("display_name"),
                    "lat": float(item.get("lat")),
                    "lon": float(item.get("lon")),
                    "boundingbox": [float(x) for x in item.get("boundingbox", [])]
                })
            return results
        return []
    except Exception as e:
        return []
