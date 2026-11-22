import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from backend.app.database.session import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    module_type = Column(String, nullable=False, index=True)
    study_area_id = Column(String, ForeignKey("study_areas.id"), nullable=False)
    job_id = Column(String, ForeignKey("analysis_jobs.id"), nullable=True)
    alert_type = Column(String, nullable=False)   # SPECTRAL_DISTURBANCE, UNUSUAL_RIVERBED_CHANGE, etc.
    severity = Column(String, nullable=False, default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    description = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False, default=0.75)
    validation_status = Column(String, nullable=False, default="PENDING_FIELD_VERIFICATION")
    geometry = Column(JSON, nullable=True) # GeoJSON anomaly polygon
    created_at = Column(DateTime, default=datetime.utcnow)
