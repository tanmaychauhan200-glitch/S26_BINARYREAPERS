# SYSTEM ARCHITECTURE — TERRAWATCH 360

```mermaid
flowchart TD
    subgraph Data_Layer ["1. Satellite & Geospatial Data Providers"]
        CDSE["Copernicus Data Space Ecosystem (Sentinel-2 L2A / Sentinel-1 GRD)"]
        Bhoonidhi["ISRO Bhoonidhi (Resourcesat AWiFS / Sentinel / Cartosat)"]
        VEDAS["ISRO VEDAS (Thematic WMS / NDVI Time Series)"]
        Bhuvan["ISRO Bhuvan (LULC & Vector Reference)"]
        LocalCache["Local Scene Store & GeoPackage Archive"]
    end

    subgraph Ingestion_Engine ["2. Ingestion & Preprocessing Core (FastAPI / Python)"]
        STAC_Client["STAC Provider Adapter & Catalog Query"]
        Downloader["Resilient Scene Ingest & Window Cropper"]
        CRS_Aligner["Reprojection & Alignment Engine (PyProj / Rasterio)"]
        Cloud_Masker["SCL / Quality Bitmask & Masking Engine"]
        Raster_Ops["Normalized Difference Indices & Spectral Math (NumPy)"]
    end

    subgraph Module_Processors ["3. Specialized Domain Processors"]
        RiverEngine["RiverWatch Engine\n(Channel Migration, Sandbar Area, Transect Width)"]
        WetlandEngine["WetlandWatch Engine\n(Water Occurrence, Persistence, Seasonal Buffer)"]
        ForestEngine["ForestGuard Engine\n(Disturbance Alerts, Fragmentation Metrics, dNDVI)"]
        UrbanEngine["UrbanWatch Engine\n(NDBI Built-up Sprawl, Proximity Buffers)"]
    end

    subgraph Storage_Layer ["4. Persistence & Export"]
        SQLite_DB[("SQLite Metadata & Job Queue (SQLAlchemy)")]
        GeoTIFF_Store[("GeoTIFF Output Rasters (COG / Pyramids)")]
        GeoJSON_Store[("Vector Anomaly Polygons (GeoJSON / GPKG)")]
        Report_Gen["Summary Reporting Engine (CSV / JSON / PDF)"]
    end

    subgraph UI_Layer ["5. Space-Themed Tactical Frontend (React + Vite + Leaflet)"]
        Dashboard["Mission Control Dashboard"]
        InteractiveMap["Multi-Layer Leaflet GIS Canvas (Split-Screen Swipe)"]
        ModuleWorkspaces["Domain Workspaces (River, Wetland, Forest, Urban)"]
        AnalyticsInspector["Temporal Analytics & Spectral Charts (Recharts)"]
        JobManager["Task Status & Download Monitor"]
    end

    Data_Layer --> STAC_Client
    Data_Layer --> LocalCache
    LocalCache --> Downloader
    STAC_Client --> Downloader
    Downloader --> CRS_Aligner --> Cloud_Masker --> Raster_Ops
    Raster_Ops --> RiverEngine
    Raster_Ops --> WetlandEngine
    Raster_Ops --> ForestEngine
    Raster_Ops --> UrbanEngine

    RiverEngine & WetlandEngine & ForestEngine & UrbanEngine --> Storage_Layer
    Storage_Layer --> Ingestion_Engine
    Ingestion_Engine <==> |REST API / JSON| UI_Layer
```

## Layer Separation and Boundaries
1. **Frontend**: Vite + React 18 + TypeScript + Tailwind CSS. Strictly presentation, client-side map interactions (AOI drawing via Leaflet Draw, layer toggling, swipe slider), and metric visualization. No raw API keys or heavy matrix manipulation on the browser.
2. **Backend Gateway**: FastAPI with async route handlers, background tasks for long-running raster computations, and clean Pydantic request/response validation.
3. **Geospatial Pipeline**: Python-based Rasterio, Shapely, PyProj, and NumPy. Vector geometries are maintained in EPSG:4326 for interchange and projected to local UTM (e.g., UTM Zone 43N/44N/45N) for area calculations.
4. **Resilience Strategy**: Fallback mock/sample provider for offline mode; live STAC client when online credentials/network are available.
