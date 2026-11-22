import logging
import requests
from typing import List, Dict, Any, Optional
from datetime import date
from backend.app.providers.base import BaseSatelliteProvider
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

class CopernicusSTACProvider(BaseSatelliteProvider):
    """
    Official Copernicus Data Space Ecosystem (CDSE) STAC Provider.
    Documentation: https://documentation.dataspace.copernicus.eu/
    Endpoint: https://stac.dataspace.copernicus.eu/v1
    """

    def __init__(self):
        self.stac_url = settings.COPERNICUS_STAC_URL
        self.token_url = settings.COPERNICUS_TOKEN_URL
        self.client_id = settings.COPERNICUS_CLIENT_ID
        self.client_secret = settings.COPERNICUS_CLIENT_SECRET
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "TerraWatch-360-EO-Engine/1.0"})

    def get_provider_id(self) -> str:
        return "copernicus"

    def check_health(self) -> Dict[str, Any]:
        """Verify CDSE STAC catalog reachability."""
        try:
            resp = self.session.get(f"{self.stac_url}", timeout=5.0)
            if resp.status_code == 200:
                return {
                    "provider": "copernicus",
                    "status": "ONLINE",
                    "code": 200,
                    "catalog_title": resp.json().get("title", "Copernicus STAC"),
                    "authenticated": bool(self.client_id and self.client_secret)
                }
            return {
                "provider": "copernicus",
                "status": "DEGRADED",
                "code": resp.status_code,
                "authenticated": False
            }
        except Exception as e:
            return {
                "provider": "copernicus",
                "status": "UNREACHABLE",
                "error": str(e),
                "authenticated": False
            }

    def search_scenes(
        self,
        bbox: Optional[List[float]] = None,
        date_start: Optional[date] = None,
        date_end: Optional[date] = None,
        max_cloud_cover: float = 20.0,
        satellite: Optional[str] = "SENTINEL-2",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Query CDSE STAC /search endpoint for Level-2A surface reflectance scenes.
        """
        search_endpoint = f"{self.stac_url}/search"
        collection = "SENTINEL-2" if satellite == "SENTINEL-2" else "SENTINEL-1"

        # Format datetime range (RFC 3339)
        dt_str = None
        if date_start and date_end:
            dt_str = f"{date_start.isoformat()}T00:00:00Z/{date_end.isoformat()}T23:59:59Z"
        elif date_start:
            dt_str = f"{date_start.isoformat()}T00:00:00Z/.."
        elif date_end:
            dt_str = f"../{date_end.isoformat()}T23:59:59Z"

        payload: Dict[str, Any] = {
            "collections": [collection],
            "limit": limit
        }
        if bbox and len(bbox) == 4:
            payload["bbox"] = bbox
        if dt_str:
            payload["datetime"] = dt_str
        if max_cloud_cover is not None and collection == "SENTINEL-2":
            payload["query"] = {
                "eo:cloud_cover": {"lte": max_cloud_cover}
            }

        try:
            resp = self.session.post(search_endpoint, json=payload, timeout=8.0)
            if resp.status_code == 200:
                stac_data = resp.json()
                features = stac_data.get("features", [])
                standardized = []
                for feat in features:
                    props = feat.get("properties", {})
                    standardized.append({
                        "product_id": feat.get("id"),
                        "provider": "copernicus",
                        "satellite": props.get("platform", "Sentinel-2"),
                        "sensor": props.get("instruments", ["MSI"])[0] if props.get("instruments") else "MSI",
                        "acquisition_date": props.get("datetime", "")[:10],
                        "cloud_cover_pct": props.get("eo:cloud_cover", 0.0),
                        "processing_level": props.get("processing:level", "LEVEL-2A"),
                        "footprint": feat.get("geometry"),
                        "assets": feat.get("assets", {})
                    })
                return standardized
            else:
                logger.warning("CDSE STAC query returned status %d: %s", resp.status_code, resp.text[:200])
                return []
        except Exception as e:
            logger.warning("CDSE STAC search failed or timed out: %s. Falling back to benchmark cache.", str(e))
            return []

    def get_scene_metadata(self, product_id: str) -> Optional[Dict[str, Any]]:
        try:
            resp = self.session.get(f"{self.stac_url}/collections/SENTINEL-2/items/{product_id}", timeout=6.0)
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception:
            return None
