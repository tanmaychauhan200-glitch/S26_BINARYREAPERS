# DATABASE SCHEMA SPECIFICATION — TERRAWATCH 360

The application uses SQLite as its default zero-configuration relational engine, structured with a clean data-access layer that can transparently scale to PostgreSQL / PostGIS.

---

### Entity-Relationship Diagram

```mermaid
erDiagram
    STUDY_AREAS ||--o{ SATELLITE_SCENES : contains
    STUDY_AREAS ||--o{ ANALYSIS_JOBS : targets
    SATELLITE_SCENES ||--o{ ANALYSIS_JOBS : "before_scene"
    SATELLITE_SCENES ||--o{ ANALYSIS_JOBS : "after_scene"
    ANALYSIS_JOBS ||--|| ANALYSIS_RESULTS : produces
    ANALYSIS_JOBS ||--o{ ALERTS : triggers
    DATA_SOURCES ||--o{ SATELLITE_SCENES : originates

    STUDY_AREAS {
        string id PK
        string name
        string description
        string module_type
        json geometry_geojson
        float area_ha
        string state
        datetime created_at
    }

    DATA_SOURCES {
        string id PK
        string provider_name
        string provider_type
        string connection_status
        json configuration_json
        datetime last_checked
    }

    SATELLITE_SCENES {
        string id PK
        string provider_id FK
        string satellite
        string sensor
        string product_id
        date acquisition_date
        float cloud_cover_pct
        string processing_level
        string crs
        float resolution_m
        json footprint_geojson
        string download_status
        string local_path
        json metadata_json
    }

    ANALYSIS_JOBS {
        string id PK
        string module_type
        string study_area_id FK
        string scene_before_id FK
        string scene_after_id FK
        string status
        float progress_pct
        datetime started_at
        datetime completed_at
        json parameters_json
        string error_message
    }

    ANALYSIS_RESULTS {
        string id PK
        string job_id FK
        string result_type
        string raster_path
        string vector_geojson_path
        float total_change_ha
        json summary_metrics_json
        json quality_metadata_json
        datetime created_at
    }

    ALERTS {
        string id PK
        string module_type
        string study_area_id FK
        string job_id FK
        string alert_type
        string severity
        string description
        float confidence_score
        string validation_status
        json geometry_geojson
        datetime created_at
    }
```

---

### Key Tables & Constraints
1. **study_areas**: Stores standard pre-configured Indian study zones (Yamuna Delhi stretch, Deepor Beel, Silent Valley, Bengaluru peri-urban) plus user-drawn polygons. Geometries are GeoJSON Feature collections.
2. **satellite_scenes**: Catalogs actual scenes discovered via STAC or bundled offline datasets.
3. **analysis_jobs**: Tracks async job states: `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`.
4. **analysis_results**: References disk-persisted GeoTIFFs, vector GeoJSON polygons, and quantified surface metrics (hectares, width variances).
5. **alerts**: Stores actionable change flags with scientific cautionary categories (`POTENTIAL_DISTURBANCE`, `UNUSUAL_RIVERBED_CHANGE`, `SEASONAL_WATER_VARIATION`).
