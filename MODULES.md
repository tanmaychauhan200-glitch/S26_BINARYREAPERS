# ENVIRONMENTAL MODULES SPECIFICATION

---

## 1. RiverWatch — River Channel & Sediment Intelligence
- **Objectives**: Monitor active channel shifts, riverbank erosion/retreat, and sandbar accumulation/extraction anomalies.
- **Key Indicators**:
  - Active water extent (ha) via MNDWI.
  - Riverbank retreat rate at selected transverse transects.
  - Exposed riverbed / sandbar surface area variance.
- **Scientifically Defensible Labels**:
  - `CHANNEL_MIGRATION_DETECTED`
  - `EXPOSED_SEDIMENT_AREA_INCREASED`
  - `RIVERBANK_RETREAT_INDICATOR`
  - `UNUSUAL_RIVERBED_CHANGE_INVESTIGATION_REQUIRED`

---

## 2. WetlandWatch — Wetland & Lake Waterbody Intelligence
- **Objectives**: Track surface water persistence, permanent vs. seasonal water shrinkage, and buffer zone encroachment.
- **Key Indicators**:
  - Water Occurrence Index (%) across multi-temporal baselines.
  - Permanent waterbody shrinkage (ha).
  - Seasonal inundation contraction.
- **Scientifically Defensible Labels**:
  - `SEASONAL_WATER_CONTRACTION`
  - `PERMANENT_WATER_LOSS_CANDIDATE`
  - `WETLAND_BUFFER_ENCROACHMENT`

---

## 3. ForestGuard — Canopy Disturbance & Fragmentation
- **Objectives**: Detect canopy degradation, canopy gaps, and patch fragmentation.
- **Key Indicators**:
  - Differenced NDVI ($\text{dNDVI}$).
  - Patch count & mean patch size (Fragstats metric).
  - Edge density & patch isolation index.
- **Scientifically Defensible Labels**:
  - `SPECTRAL_DISTURBANCE_ALERT`
  - `POTENTIAL_CANOPY_GAP`
  - `FRAGMENTATION_INDEX_INCREASE`

---

## 4. UrbanWatch — Sprawl & Sensitive Zone Proximity
- **Objectives**: Map impervious surface expansion and monitor proximity to eco-sensitive areas.
- **Key Indicators**:
  - New built-up area (ha) via NDBI & MNDWI negation.
  - Distance to nearest waterbody / forest boundary (m).
  - Built-up density within 500m ecological buffer.
- **Scientifically Defensible Labels**:
  - `BUILT_UP_EXPANSION_DETECTED`
  - `NEW_IMPERVIOUS_SURFACE_CANDIDATE`
  - `EXPANSION_NEAR_SENSITIVE_BUFFER`
