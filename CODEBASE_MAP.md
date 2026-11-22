# CODEBASE DIRECTORY MAP — TERRAWATCH 360

```
terrawatch/
├── README.md                           # Main landing documentation
├── PROJECT_OVERVIEW.md                 # Project vision, domains, and stakeholders
├── ARCHITECTURE.md                     # System architecture & Mermaid flowcharts
├── CODEBASE_MAP.md                     # File directory and responsibility map
├── DATABASE_SCHEMA.md                  # SQLite / Spatial database structure
├── API_REFERENCE.md                    # FastAPI endpoint contracts & payloads
├── SATELLITE_DATA_SOURCES.md           # Copernicus, ISRO Bhoonidhi, VEDAS, Bhuvan guides
├── PROCESSING_PIPELINE.md              # Ingestion, preprocessing, and classification flow
├── ALGORITHMS.md                       # Formulas (NDWI, MNDWI, NDVI, NDBI, Fragstats)
├── UI_UX_GUIDE.md                      # Tactical space theme, colors, and layout specs
├── MODULES.md                          # RiverWatch, WetlandWatch, ForestGuard, UrbanWatch
├── CONFIGURATION.md                    # Environment variables and system thresholds
├── INSTALLATION.md                     # Windows installation guide (Conda / Node)
├── TESTING.md                          # Test execution procedures and test cases
├── DEVELOPMENT_LOG.md                  # Chronological engineering log
├── KNOWN_LIMITATIONS.md                # Implemented, partial, and planned items
├── DEMO_GUIDE.md                       # Scripted step-by-step hackathon demo walk-through
├── DECISIONS.md                        # Architectural Decision Records (ADRs)
│
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI application entry point
│   │   ├── core/
│   │   │   ├── config.py               # Pydantic Settings & environment variables
│   │   │   ├── logging.py              # Structured application logger
│   │   │   └── security.py             # Input sanitization and path validation
│   │   ├── database/
│   │   │   ├── session.py              # SQLite / SQLAlchemy engine & session factory
│   │   │   └── init_db.py              # Schema generation & seed study areas
│   │   ├── models/
│   │   │   ├── study_area.py           # Study area geometries & state metadata
│   │   │   ├── satellite_scene.py      # Scene metadata, cloud cover, sensor, CRS
│   │   │   ├── analysis_job.py         # Background worker queue status
│   │   │   ├── analysis_result.py      # Output file references, calculated metrics
│   │   │   └── alert.py                # Classified environmental disturbance records
│   │   ├── schemas/
│   │   │   ├── common.py               # GeoJSON & standard response envelopes
│   │   │   ├── scenes.py               # Scene search queries and filters
│   │   │   └── analysis.py             # Job submission & progress payloads
│   │   ├── api/
│   │   │   ├── router.py               # Main API aggregation router
│   │   │   ├── endpoints/
│   │   │   │   ├── health.py           # Health check & system diagnostics
│   │   │   │   ├── study_areas.py      # Study area CRUD & sample geometries
│   │   │   │   ├── providers.py        # STAC search, provider status & connectivity
│   │   │   │   ├── jobs.py             # Analysis execution & progress tracking
│   │   │   │   ├── results.py          # Results queries, rasters, and GeoJSON vectors
│   │   │   │   └── exports.py          # CSV and report download generation
│   │   ├── providers/
│   │   │   ├── base.py                 # Abstract Base Provider interface
│   │   │   ├── copernicus_stac.py      # Copernicus Data Space Ecosystem STAC connector
│   │   │   ├── bhoonidhi_stac.py       # ISRO Bhoonidhi STAC adapter
│   │   │   ├── isro_wms.py             # VEDAS & Bhuvan WMS reference connector
│   │   │   └── offline_provider.py     # Local pre-packaged sample scene provider
│   │   ├── geospatial/
│   │   │   ├── reader.py               # Windowed GeoTIFF reader
│   │   │   ├── crs.py                  # Projections, UTM auto-detection, PyProj
│   │   │   ├── cloud_mask.py           # SCL and threshold masking
│   │   │   ├── indices.py              # NDWI, MNDWI, NDVI, NDBI calculations
│   │   │   └── vectorizer.py           # Polygonization and contour extraction
│   │   ├── modules/
│   │   │   ├── riverwatch/
│   │   │   │   └── processor.py        # Riverbank retreat & sandbar area analysis
│   │   │   ├── wetlandwatch/
│   │   │   │   └── processor.py        # Water persistence & seasonal shrinkage analysis
│   │   │   ├── forestguard/
│   │   │   │   └── processor.py        # Canopy disturbance & patch fragmentation
│   │   │   └── urbanwatch/
│   │   │       └── processor.py        # Impervious expansion & sensitive buffer analysis
│   │   └── utils/
│   │       └── geo_calc.py             # Geodesic & UTM area calculations in hectares
│   ├── tests/
│   │   ├── conftest.py                 # Pytest fixtures & synthetic rasters
│   │   ├── test_indices.py             # Unit tests for spectral indices
│   │   ├── test_riverwatch.py          # Unit tests for RiverWatch processor
│   │   ├── test_wetlandwatch.py        # Unit tests for WetlandWatch processor
│   │   ├── test_forestguard.py         # Unit tests for ForestGuard processor
│   │   ├── test_urbanwatch.py          # Unit tests for UrbanWatch processor
│   │   └── test_api.py                 # FastAPI TestClient endpoints verification
│   └── requirements.txt                # Pinned backend dependencies
│
├── frontend/
│   ├── index.html                      # Single page application host
│   ├── vite.config.ts                  # Vite build configuration & proxy
│   ├── tailwind.config.js              # Space-inspired theme colors & typography
│   ├── package.json                    # Frontend dependencies & scripts
│   └── src/
│       ├── App.tsx                     # Top-level routing and state layout
│       ├── main.tsx                    # React DOM entry point
│       ├── index.css                   # Space theme global styles
│       ├── components/
│       │   ├── Navbar.tsx              # Mission control header
│       │   ├── ModuleCard.tsx          # 4 module navigation cards
│       │   ├── StatusBadge.tsx         # Provider and job status indicators
│       │   ├── SplitSlider.tsx         # Before/after swipe comparison widget
│       │   └── MetricWidget.tsx        # High-impact metric counters
│       ├── layouts/
│       │   └── MainLayout.tsx          # Global mission control layout
│       ├── maps/
│       │   ├── MapCanvas.tsx           # Leaflet interactive map with layer toggles
│       │   ├── AOISelector.tsx         # Polygon drawing & study-area selector
│       │   └── Legend.tsx              # Dynamic scientific classification legend
│       ├── charts/
│       │   └── TrendChart.tsx          # Recharts temporal change visualizer
│       ├── modules/
│       │   ├── riverwatch/             # Dedicated RiverWatch view
│       │   ├── wetlandwatch/           # Dedicated WetlandWatch view
│       │   ├── forestguard/            # Dedicated ForestGuard view
│       │   └── urbanwatch/             # Dedicated UrbanWatch view
│       ├── services/
│       │   ├── api.ts                  # Axios/fetch backend communication
│       │   └── providers.ts            # Scene search and provider status calls
│       └── types/
│           └── index.ts                # TypeScript interfaces for scenes, jobs, alerts
│
├── data/
│   ├── raw/                            # Ingested scenes (Sentinel / Landsat)
│   ├── intermediate/                   # Clipped and masked rasters
│   ├── processed/                      # Classified rasters & indices
│   └── test/                           # Synthetic rasters for unit tests
│
└── outputs/
    ├── maps/                           # Rendered web map tiles / preview PNGs
    └── reports/                        # Exported CSV and analytical summaries
```
