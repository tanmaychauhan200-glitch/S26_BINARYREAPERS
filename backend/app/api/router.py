from fastapi import APIRouter
from backend.app.api.endpoints import health, study_areas, providers, jobs, results, alerts, analysis

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(study_areas.router, prefix="/study-areas", tags=["Study Areas"])
api_router.include_router(providers.router, prefix="/providers", tags=["Providers & Satellite Scenes"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Analysis Jobs"])
api_router.include_router(results.router, prefix="/results", tags=["Analysis Results"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Environmental Alerts"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["AI & Point Analysis"])
