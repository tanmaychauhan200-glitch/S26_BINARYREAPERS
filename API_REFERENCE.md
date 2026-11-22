# API REFERENCE — TERRAWATCH 360 REST BACKEND

Base URL: `http://localhost:8000/api/v1`

---

## 1. System & Health
### `GET /health`
Returns system status, active database engine, and registered geospatial libraries.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "geospatial_engine": {
    "numpy": "2.x",
    "pyproj": "active",
    "raster_support": "active"
  },
  "timestamp": "2026-11-22T03:30:00Z"
}
```

---

## 2. Study Areas
### `GET /study-areas`
Returns all registered Indian benchmark study areas and custom user AOIs.
Optional query parameter: `?module=riverwatch`

### `POST /study-areas`
Register a user-drawn Area of Interest (AOI).
**Request Body:**
```json
{
  "name": "Yamuna Okhla Reach",
  "description": "Downstream Okhla barrage riverbed observation",
  "module_type": "riverwatch",
  "state": "Delhi / UP",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[77.29, 28.53], [77.34, 28.53], [77.34, 28.58], [77.29, 28.58], [77.29, 28.53]]]
  }
}
```

---

## 3. Satellite Data & Providers
### `GET /providers/status`
Returns connectivity, quota, and authentication status for external providers.

### `POST /providers/search`
Query Copernicus STAC / Bhoonidhi for available scenes over an AOI.
**Request Body:**
```json
{
  "provider": "copernicus",
  "aoi_geometry": { ... },
  "date_start": "2023-01-01",
  "date_end": "2024-03-31",
  "max_cloud_cover": 20.0,
  "satellite": "sentinel-2"
}
```

---

## 4. Analysis Jobs
### `POST /jobs/run`
Submit an environmental change-detection analysis job.
**Request Body:**
```json
{
  "module_type": "riverwatch",
  "study_area_id": "study_yamuna_delhi",
  "scene_before_id": "scene_s2_20230215",
  "scene_after_id": "scene_s2_20240220",
  "parameters": {
    "ndwi_threshold": 0.05,
    "sandbar_threshold": 0.12,
    "min_patch_size_ha": 0.5
  }
}
```

### `GET /jobs/{job_id}`
Query job progress, status (`PENDING`, `RUNNING`, `COMPLETED`, `FAILED`), and diagnostic logs.

---

## 5. Results & Analytical Overlays
### `GET /results/{job_id}`
Retrieve computed statistics, summary indicators, and change metrics.

### `GET /results/{job_id}/vector`
Returns the classified change polygons in GeoJSON format for Leaflet overlay.

### `GET /results/{job_id}/raster-preview`
Returns a rendered web-ready PNG/RGBA tile layer for split-screen swipe inspection.

### `GET /results/{job_id}/export/{format}`
Download reports in CSV, GeoJSON, or summary JSON formats.
