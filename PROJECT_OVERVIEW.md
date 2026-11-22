# PROJECT OVERVIEW — TERRAWATCH 360

## 1. Executive Summary & Vision
TerraWatch 360 is an integrated, scientific-grade satellite Earth Observation (EO) and environmental change-intelligence platform. It equips environmental authorities, river basin managers, wetland conservationists, forestry departments, urban planning bodies, and researchers across India with actionable spatial evidence.

### Core Philosophy:
- **Decision-Support, Not Automated Accusation**: Space data highlights optical and microwave reflectance anomalies; it does not replace jurisdictional ground verification or legal compliance auditing.
- **Scientific Rigor**: Pixel counts are converted to physical surface areas using projected coordinate reference systems (local UTM zones) and actual spatial resolutions.
- **Provider Redundancy**: If external APIs experience downtime or quota caps, the system falls back seamlessly to authenticated caches or manual scene ingestion without application crashes.

---

## 2. The Four Specialized Pillars

| Module | Core Domain | Flagship Geographical Focus | Key Methodologies |
| :--- | :--- | :--- | :--- |
| **RiverWatch** | River dynamics, active riverbed sediment extraction monitoring, channel shifts | Yamuna (Delhi/Haryana), Ganga (Haridwar/Varanasi), Brahmaputra | NDWI, MNDWI, Morphological water masks, multi-date transect width variance |
| **WetlandWatch** | Wetland shrinkage, seasonal persistence, ecological buffer encroachment | Deepor Beel (Assam), Chilika Lake (Odisha), Keoladeo (Rajasthan) | Multi-temporal MNDWI, water occurrence frequency, seasonal baseline indexing |
| **ForestGuard** | Canopy degradation, vegetation disturbance alerts, patch connectivity | Western Ghats (Silent Valley/Wayanad), Hasdeo Arand (Chhattisgarh) | dNDVI, NBR (burn/clearing), EVI, Fragstats-inspired patch density & connectivity |
| **UrbanWatch** | Urban sprawl, impervious surface dynamics, peri-urban encroachment | Bengaluru outskirts, Delhi NCR peri-urban corridor, Hyderabad HMDA | NDBI, MNDWI-NDVI masking, morphological dilation & buffer zoning |

---

## 3. Target End Users
1. **Central & State Pollution Control Boards (CPCB / SPCB)**
2. **Ministry of Environment, Forest and Climate Change (MoEFCC)**
3. **State Remote Sensing Application Centres** (e.g., HARSAC, ARSAC, ORSAC)
4. **Water Resource & Irrigation Departments**
5. **Urban Planning Authorities (DDA, BDA, etc.)**
6. **Academic Geospatial Researchers & Conservation NGOs**

---

## 4. Hackathon Competitive Advantages
1. **Unified Common Core**: Instead of 4 disparate demos, a single cohesive high-performance engine powers all 4 domains.
2. **True Provenance & Authenticity**: Every alert tracks acquisition satellite, orbit, tile, sensor, processing timestamp, and quality metadata (SCL cloud masking).
3. **Space-Grade Command & Control UI**: Dark-themed, high-contrast tactical GIS interface inspired by NASA Earth Observatory and ESA Copernicus dashboards.
4. **Resilient Offline Fallback**: Bundled genuine pre-computed benchmark scenes ensuring flawless demonstration even without high-bandwidth internet.
