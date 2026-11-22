# SATELLITE DATA SOURCES & PROVIDER ARCHITECTURE

TerraWatch 360 integrates multi-source Earth Observation datasets using a modular provider-adapter pattern.

---

## 1. Copernicus Data Space Ecosystem (CDSE) — Primary Source
- **Website**: https://dataspace.copernicus.eu/
- **Documentation**: https://documentation.dataspace.copernicus.eu/
- **Public STAC Catalog Endpoint**: `https://stac.dataspace.copernicus.eu/v1/`
- **Sensors Used**:
  - **Sentinel-2 MSI Level-2A (Bottom-of-Atmosphere Surface Reflectance)**: 10m visible & NIR bands (B02, B03, B04, B08), 20m SWIR bands (B11, B12), and Scene Classification Layer (SCL) for cloud/shadow masking.
  - **Sentinel-1 C-SAR GRD (Ground Range Detected)**: High-resolution dual-pol (VV + VH) for all-weather flood & waterbody delineation when monsoon clouds impede optical sensors.
- **Authentication**: Free registration via Copernicus OpenID Connect. Token endpoint: `https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token`.
- **Licensing & Terms**: Free, full, and open data under Copernicus Regulation.

---

## 2. ISRO Bhoonidhi — Indian Satellite Source
- **Website**: https://bhoonidhi.nrsc.gov.in/
- **API Documentation**: https://bhoonidhi.nrsc.gov.in/bhoonidhi-api/
- **Data Collections**:
  - Resourcesat-2 & 2A AWiFS (Advanced Wide Field Sensor, 56m, 5-day revisit) for broad-scale national forest canopy and river basin monitoring.
  - LISS-III / LISS-IV for high-resolution targeted assessments.
- **Access Protocol**: Requires registered Bhoonidhi credentials, token-based authorization.
- **Integration Role**: Supplementary catalog search and Indian satellite scene metadata discovery.

---

## 3. ISRO VEDAS — Analytical Reference
- **Website**: https://www.vedas.sac.gov.in/vconsole/
- **Services Used**:
  - Thematic WMS layers for NDVI time series and agricultural/wetland reference masks.
  - Multi-temporal vegetation index comparisons over Indian agro-ecological zones.

---

## 4. ISRO Bhuvan — Contextual Geospatial Layers
- **Website**: https://bhuvan-app1.nrsc.gov.in/api/index.php
- **Layers Integrated**:
  - National Land Use / Land Cover (LULC) 1:50k reference WMS layers.
  - Waterbodies information system and watershed boundaries.

---

## 5. Offline Demo Cache & Graceful Degradation
To guarantee zero-failure presentations during hackathons or network disruptions:
- A curated repository of authentic pre-downloaded Sentinel-2 L2A scenes for 4 benchmark Indian test regions is bundled in `data/test/` and `data/raw/`.
- If CDSE/Bhoonidhi endpoints return HTTP 429 (quota), 503 (maintenance), or network timeout, the application seamlessly switches to the Offline Benchmark Provider without interrupting the user.
