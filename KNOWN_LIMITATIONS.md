# KNOWN LIMITATIONS & SCIENTIFIC SAFEGUARDS

---

## 1. Scientific & Geospatial Safeguards
1. **Decision Support Only**: TerraWatch 360 detects spectral anomalies and surface physical changes. It does not certify legal violations, land titles, or environmental crime.
2. **Atmospheric & Cloud Contamination**: Cloud shadows and thin cirrus can depress NDVI and cause false water detections. The SCL mask reduces but does not completely eliminate cloud boundary artifacts.
3. **Seasonal vs. Permanent Change**: A drop in water area or vegetative greenness between pre-monsoon and post-monsoon is normal phenological behavior. Comparisons must only be performed on seasonally harmonized baselines.

---

## 2. Technical Scope & Implementation Status

| Feature | Status | Notes |
| :--- | :--- | :--- |
| Core Architecture & Database Models | **COMPLETED** | SQLite & SQLAlchemy async design |
| Sentinel-2 L2A STAC Connector | **COMPLETED** | CDSE STAC client with fallback cache |
| Indian UTM & CRS Projector | **COMPLETED** | Auto-detection for zones 43N/44N/45N/46N |
| Spectral Indices & Noise Filters | **COMPLETED** | NDWI, MNDWI, NDVI, NDBI & morphology |
| 4 Domain Geospatial Processors | **COMPLETED** | RiverWatch, WetlandWatch, ForestGuard, UrbanWatch |
| Split-Screen GIS Swipe UI | **COMPLETED** | Leaflet with custom touch/pointer slider |
| Vector GeoJSON & CSV Exports | **COMPLETED** | Real client-side dynamic downloads |
| SAR Terrain & Speckle Filtering | *Planned Phase 2* | Baseline GRD dual-pol supported |
| PostGIS Multi-Node Cluster | *Future Expansion* | Architecture abstract for PostgreSQL |
