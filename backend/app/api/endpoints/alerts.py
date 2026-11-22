from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.alert import Alert
from backend.app.schemas.alert import AlertResponse

router = APIRouter()

@router.get("", response_model=List[AlertResponse])
def list_alerts(
    module_type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Alert)
    if module_type:
        query = query.filter(Alert.module_type == module_type)
    if severity:
        query = query.filter(Alert.severity == severity)
    return query.order_by(Alert.created_at.desc()).limit(50).all()
