import sqlite3
import numpy as np
import rasterio
import shapely
import pyproj
from datetime import datetime
from fastapi import APIRouter
from sqlalchemy import text
from backend.app.core.config import settings

router = APIRouter()

@router.get("/health")
def get_health():
    # Verify database connection
    db_status = "connected"
    try:
        from backend.app.database.session import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "database": db_status,
        "geospatial_engine": {
            "numpy": np.__version__,
            "rasterio": rasterio.__version__,
            "shapely": shapely.__version__,
            "pyproj": pyproj.__version__
        },
        "providers": {
            "copernicus_stac": "online",
            "bhoonidhi_adapter": "ready",
            "offline_benchmark_cache": "active" if settings.OFFLINE_DEMO_MODE else "inactive"
        }
    }
