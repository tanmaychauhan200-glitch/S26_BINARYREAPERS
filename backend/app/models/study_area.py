import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, JSON
from backend.app.database.session import Base

class StudyArea(Base):
    __tablename__ = "study_areas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    module_type = Column(String, nullable=False, index=True)  # riverwatch, wetlandwatch, forestguard, urbanwatch
    state = Column(String, nullable=False)
    geometry = Column(JSON, nullable=False)  # GeoJSON Polygon / MultiPolygon
    area_ha = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
