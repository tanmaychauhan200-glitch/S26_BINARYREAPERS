# ARCHITECTURAL DECISION RECORDS (ADR)

---

## ADR 001: SQLite as MVP Relational Engine
- **Context**: Need lightweight, zero-configuration local database for metadata, job queue, and alerts without requiring heavy Docker or PostgreSQL setup on Windows.
- **Decision**: Use SQLite with SQLAlchemy ORM.
- **Consequences**: Fast setup, single file portability (`terrawatch.db`), zero cloud cost. Easy to transition to PostgreSQL/PostGIS in future versions.

---

## ADR 002: NumPy and Rasterio as Core Geospatial Engine
- **Context**: Performing matrix spectral operations (NDWI, MNDWI, NDVI, NDBI) and raster clipping across Sentinel-2 bands.
- **Decision**: Standardize on Rasterio + NumPy array vectorization with PyProj for CRS transformations.
- **Consequences**: Extremely high performance, deterministic calculations, zero external SaaS dependencies.

---

## ADR 003: Copernicus STAC + Local Benchmark Cache Dual-Strategy
- **Context**: External satellite APIs (CDSE, Bhoonidhi) can experience quota limits, network latency, or maintenance during live hackathon demos.
- **Decision**: Build a provider-agnostic STAC interface that seamlessly switches to a local genuine benchmark scene repository if live API calls fail or latency exceeds threshold.
- **Consequences**: Zero risk of demo failure; 100% genuine satellite data provenance preserved.

---

## ADR 004: Cautious Non-Accusatory Terminology
- **Context**: Remote sensing cannot verify legal permits or on-ground administrative authorizations.
- **Decision**: Avoid labels like "illegal sand mining" or "unauthorized deforestation". Use descriptive labels such as "unusual riverbed change requiring field investigation" and "spectral canopy disturbance".
- **Consequences**: Scientific credibility, legal defensibility, and compliance with hackathon evaluation standards.
