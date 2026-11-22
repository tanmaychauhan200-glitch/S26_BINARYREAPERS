import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Float, DateTime, Date, JSON
from backend.app.database.session import Base

class SatelliteScene(Base):
    __tablename__ = "satellite_scenes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String, nullable=False, default="copernicus")
    satellite = Column(String, nullable=False)  # Sentinel-2A, Sentinel-2B, Sentinel-1A, Resourcesat-2
    sensor = Column(String, nullable=False)     # MSI, C-SAR, AWiFS
    product_id = Column(String, nullable=False, unique=True, index=True)
    acquisition_date = Column(Date, nullable=False, index=True)
    cloud_cover_pct = Column(Float, nullable=False, default=0.0)
    processing_level = Column(String, nullable=False, default="LEVEL-2A")
    crs = Column(String, nullable=False, default="EPSG:4326")
    resolution_m = Column(Float, nullable=False, default=10.0)
    footprint = Column(JSON, nullable=False)    # GeoJSON Polygon
    download_status = Column(String, nullable=False, default="AVAILABLE")  # AVAILABLE, DOWNLOADING, DOWNLOADED, FAILED
    local_path = Column(String, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
