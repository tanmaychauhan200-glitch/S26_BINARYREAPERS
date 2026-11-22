# REMOTE SENSING ALGORITHMS & MATHEMATICAL FORMULATIONS

---

## 1. Normalized Spectral Indices

### A. Normalized Difference Water Index (NDWI) — McFeeters (1996)
$$\text{NDWI} = \frac{\rho_{\text{Green}} - \rho_{\text{NIR}}}{\rho_{\text{Green}} + \rho_{\text{NIR}}} = \frac{\text{B03} - \text{B08}}{\text{B03} + \text{B08}}$$
- Water features typically exhibit $\text{NDWI} > 0.0$.
- Terrestrial vegetation and bare soil yield negative values.

### B. Modified Normalized Difference Water Index (MNDWI) — Xu (2006)
$$\text{MNDWI} = \frac{\rho_{\text{Green}} - \rho_{\text{SWIR}}}{\rho_{\text{Green}} + \rho_{\text{SWIR}}} = \frac{\text{B03} - \text{B11}}{\text{B03} + \text{B11}}$$
- Significantly reduces false positives over built-up urban structures compared to NDWI.
- Crucial for wetland and river channel extraction near urban centers.

### C. Normalized Difference Vegetation Index (NDVI) — Rouse et al. (1974)
$$\text{NDVI} = \frac{\rho_{\text{NIR}} - \rho_{\text{Red}}}{\rho_{\text{NIR}} + \rho_{\text{Red}}} = \frac{\text{B08} - \text{B04}}{\text{B08} + \text{B04}}$$
- Healthy dense forest canopy: $0.6 \le \text{NDVI} \le 0.9$.
- Degraded / scrub vegetation: $0.2 \le \text{NDVI} < 0.4$.
- Bare soil / rock / sandbar: $0.05 \le \text{NDVI} < 0.2$.

### D. Normalized Difference Built-Up Index (NDBI) — Zha et al. (2003)
$$\text{NDBI} = \frac{\rho_{\text{SWIR}} - \rho_{\text{NIR}}}{\rho_{\text{SWIR}} + \rho_{\text{NIR}}} = \frac{\text{B11} - \text{B08}}{\text{B11} + \text{B08}}$$
- Impervious surfaces, concrete, and construction sites exhibit positive NDBI while vegetation yields negative values.

---

## 2. Module-Specific Analytical Formulations

### Module 1: RiverWatch
1. **Water Extent Mask**: $M_{\text{water}} = (\text{MNDWI} > T_{\text{water}})$ where $T_{\text{water}} \approx 0.05$.
2. **Exposed Sandbar / Sediment Mask**:
   $$M_{\text{sandbar}} = (\text{NDVI} < 0.25) \land (\text{MNDWI} < 0.0) \land (\rho_{\text{Red}} > 0.15) \land (\text{DistanceToWater} \le D_{\text{corridor}})$$
3. **Riverbank Retreat / Migration**:
   $$\Delta M_{\text{bank}} = M_{\text{water}}(t_2) \setminus M_{\text{water}}(t_1)$$
   Identifies newly inundated banks (erosion/retreat).

### Module 2: WetlandWatch
1. **Water Persistence Frequency ($F_w$)**:
   $$F_w(x, y) = \frac{1}{N} \sum_{i=1}^{N} M_{\text{water}}(x, y, t_i)$$
   - Permanent water: $F_w \ge 0.75$.
   - Seasonal water: $0.25 \le F_w < 0.75$.
   - Ephemeral inundation: $F_w < 0.25$.
2. **Wetland Shrinkage Index**:
   $$\Delta A_{\text{wetland}} = A_{\text{permanent}}(t_1) - A_{\text{permanent}}(t_2)$$

### Module 3: ForestGuard
1. **Differenced NDVI ($\text{dNDVI}$)**:
   $$\text{dNDVI} = \text{NDVI}(t_1) - \text{NDVI}(t_2)$$
   - Severe disturbance / canopy loss: $\text{dNDVI} > 0.25$.
   - Moderate disturbance: $0.15 < \text{dNDVI} \le 0.25$.
   - Regrowth / canopy recovery: $\text{dNDVI} < -0.15$.
2. **Landscape Fragmentation Index ($LFI$)**:
   $$LFI = \frac{\text{Number of Patches}}{\text{Total Forest Area (ha)}}$$
   Monitors connectivity loss and patch breakup over time.

### Module 4: UrbanWatch
1. **Impervious Surface Mask ($M_{\text{urban}}$)**:
   $$M_{\text{urban}} = (\text{NDBI} > \text{NDVI}) \land (\text{MNDWI} < 0.0)$$
2. **New Built-up Encroachment**:
   $$\Delta M_{\text{urban}} = M_{\text{urban}}(t_2) \land \neg M_{\text{urban}}(t_1)$$
3. **Ecological Buffer Proximity**:
   Intersects $\Delta M_{\text{urban}}$ with distance buffers ($100\text{m}, 500\text{m}, 1000\text{m}$) surrounding declared wetland and forest boundaries.
