from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import date

class BaseSatelliteProvider(ABC):
    """
    Abstract Base Class for satellite data providers (Copernicus CDSE, Bhoonidhi, Offline).
    Enforces unified discovery, metadata inspection, availability checks, and asset ingestion.
    """

    @abstractmethod
    def get_provider_id(self) -> str:
        """Returns unique provider identifier (e.g. 'copernicus', 'bhoonidhi', 'offline')."""
        pass

    @abstractmethod
    def check_health(self) -> Dict[str, Any]:
        """Checks connectivity, authentication status, and quota availability."""
        pass

    @abstractmethod
    def search_scenes(
        self,
        bbox: Optional[List[float]] = None,
        date_start: Optional[date] = None,
        date_end: Optional[date] = None,
        max_cloud_cover: float = 20.0,
        satellite: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Discovers satellite scenes matching geographical bounding box and observation window.
        Returns standardized scene metadata dicts.
        """
        pass

    @abstractmethod
    def get_scene_metadata(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves complete metadata, asset links, and band specifications for a scene."""
        pass
