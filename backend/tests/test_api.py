import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "TerraWatch 360" in data["message"]

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "geospatial_engine" in data
    assert "rasterio" in data["geospatial_engine"]

def test_list_study_areas():
    response = client.get("/api/v1/study-areas")
    assert response.status_code == 200
    areas = response.json()
    assert len(areas) >= 4
    module_types = {a["module_type"] for a in areas}
    assert "riverwatch" in module_types
    assert "wetlandwatch" in module_types
    assert "forestguard" in module_types
    assert "urbanwatch" in module_types

def test_providers_status():
    response = client.get("/api/v1/providers/status")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    assert len(data["providers"]) >= 3

def test_run_analysis_job():
    payload = {
        "module_type": "riverwatch",
        "study_area_id": "study_yamuna_delhi",
        "parameters": {"ndwi_threshold": 0.05}
    }
    response = client.post("/api/v1/jobs/run", json=payload)
    assert response.status_code == 202
    job = response.json()
    assert job["module_type"] == "riverwatch"
    assert "id" in job
