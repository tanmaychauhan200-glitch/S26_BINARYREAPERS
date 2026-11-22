from typing import List, Dict, Any, Optional
from datetime import date
from backend.app.providers.base import BaseSatelliteProvider
from backend.app.database.init_db import BENCHMARK_SCENES

class OfflineBenchmarkProvider(BaseSatelliteProvider):
    """
    Offline Benchmark Provider holding verified genuine Sentinel-2 Level-2A surface reflectance
    metadata and pre-computed rasters for the 4 Indian flagship study regions.
    Guarantees 100% reliable hackathon presentation without network dependence.
    """

    def __init__(self):
        self.scenes = BENCHMARK_SCENES

    def get_provider_id(self) -> str:
        return "offline_cache"

    def check_health(self) -> Dict[str, Any]:
        return {
            "provider": "offline_cache",
            "status": "ACTIVE",
            "scenes_cached": len(self.scenes),
            "authenticated": True,
            "message": "Zero-latency local benchmark scene storage active."
        }

    def search_scenes(
        self,
        bbox: Optional[List[float]] = None,
        date_start: Optional[date] = None,
        date_end: Optional[date] = None,
        max_cloud_cover: float = 20.0,
        satellite: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        results = []
        for s in self.scenes:
            if max_cloud_cover is not None and s["cloud_cover_pct"] > max_cloud_cover:
                continue
            if date_start and s["acquisition_date"] < date_start:
                continue
            if date_end and s["acquisition_date"] > date_end:
                continue
            results.append({
                "product_id": s["product_id"],
                "provider": "offline_cache",
                "satellite": s["satellite"],
                "sensor": s["sensor"],
                "acquisition_date": s["acquisition_date"].isoformat(),
                "cloud_cover_pct": s["cloud_cover_pct"],
                "processing_level": s["processing_level"],
                "footprint": s["footprint"]
            })
            if len(results) >= limit:
                break
        return results

    def get_scene_metadata(self, product_id: str) -> Optional[Dict[str, Any]]:
        for s in self.scenes:
            if s["product_id"] == product_id or s["id"] == product_id:
                return dict(s)
        return None
