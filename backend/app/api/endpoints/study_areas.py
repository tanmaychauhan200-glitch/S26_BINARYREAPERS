from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.study_area import StudyArea
from backend.app.schemas.study_area import StudyAreaResponse, StudyAreaCreate

router = APIRouter()

@router.get("", response_model=List[StudyAreaResponse])
def list_study_areas(
    module_type: Optional[str] = Query(None, description="Filter by module: riverwatch, wetlandwatch, forestguard, urbanwatch"),
    db: Session = Depends(get_db)
):
    query = db.query(StudyArea)
    if module_type:
        query = query.filter(StudyArea.module_type == module_type)
    return query.all()

@router.get("/{study_area_id}", response_model=StudyAreaResponse)
def get_study_area(study_area_id: str, db: Session = Depends(get_db)):
    area = db.query(StudyArea).filter(StudyArea.id == study_area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Study area not found")
    return area

@router.post("", response_model=StudyAreaResponse, status_code=201)
def create_custom_study_area(payload: StudyAreaCreate, db: Session = Depends(get_db)):
    # Calculate approx area in ha from coordinates if not provided
    coords = payload.geometry.get("coordinates", [[]])[0]
    area_ha = payload.area_ha
    if area_ha <= 0 and len(coords) >= 4:
        # Simple bounding box approximation if client hasn't projected
        lons = [pt[0] for pt in coords]
        lats = [pt[1] for pt in coords]
        width_km = (max(lons) - min(lons)) * 105.0
        height_km = (max(lats) - min(lats)) * 111.0
        area_ha = round((width_km * height_km) * 100.0, 1)

    new_area = StudyArea(
        name=payload.name,
        description=payload.description or "User-defined Area of Interest",
        module_type=payload.module_type,
        state=payload.state,
        geometry=payload.geometry,
        area_ha=area_ha
    )
    db.add(new_area)
    db.commit()
    db.refresh(new_area)
    return new_area
