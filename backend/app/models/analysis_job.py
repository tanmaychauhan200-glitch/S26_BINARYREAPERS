import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from backend.app.database.session import Base

class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    module_type = Column(String, nullable=False, index=True)
    study_area_id = Column(String, ForeignKey("study_areas.id"), nullable=False)
    scene_before_id = Column(String, ForeignKey("satellite_scenes.id"), nullable=True)
    scene_after_id = Column(String, ForeignKey("satellite_scenes.id"), nullable=True)
    status = Column(String, nullable=False, default="PENDING", index=True)  # PENDING, RUNNING, COMPLETED, FAILED
    progress_pct = Column(Float, nullable=False, default=0.0)
    parameters_json = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
