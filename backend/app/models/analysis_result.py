import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from backend.app.database.session import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("analysis_jobs.id"), nullable=False, unique=True, index=True)
    result_type = Column(String, nullable=False)  # change_detection, persistence_map, canopy_loss, urban_sprawl
    raster_path = Column(String, nullable=True)   # Local GeoTIFF path
    vector_geojson_path = Column(String, nullable=True) # Local GeoJSON path
    total_change_ha = Column(Float, nullable=False, default=0.0)
    summary_metrics = Column(JSON, nullable=True) # Module-specific metrics dict
    quality_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
