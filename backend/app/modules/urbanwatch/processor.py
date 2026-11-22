import numpy as np
from typing import Dict, Any, List
from backend.app.geospatial.indices import compute_ndbi, compute_ndvi, compute_mndwi
from backend.app.geospatial.vectorizer import vectorize_binary_mask_to_geojson, filter_noise_morphology

class UrbanWatchProcessor:
    """
    Module 4: UrbanWatch
    Monitors impervious surface expansion, urban sprawl trajectories,
    and encroachment into declared agricultural and eco-sensitive wetland buffers.
    """

    def process(
        self,
        t1_bands: Dict[str, np.ndarray],
        t2_bands: Dict[str, np.ndarray],
        bbox: List[float],
        resolution_m: float = 10.0
    ) -> Dict[str, Any]:
        # Impervious surface: NDBI > NDVI and MNDWI < 0.0
        ndbi_t1 = compute_ndbi(t1_bands['swir'], t1_bands['nir'])
        ndvi_t1 = compute_ndvi(t1_bands['nir'], t1_bands['red'])
        mndwi_t1 = compute_mndwi(t1_bands['green'], t1_bands['swir'])
        builtup_t1 = (ndbi_t1 > ndvi_t1) & (mndwi_t1 < 0.0)

        ndbi_t2 = compute_ndbi(t2_bands['swir'], t2_bands['nir'])
        ndvi_t2 = compute_ndvi(t2_bands['nir'], t2_bands['red'])
        mndwi_t2 = compute_mndwi(t2_bands['green'], t2_bands['swir'])
        builtup_t2 = (ndbi_t2 > ndvi_t2) & (mndwi_t2 < 0.0)

        # New built-up expansion: Land that was not built-up in T1, but is built-up in T2
        expansion_mask = (~builtup_t1) & builtup_t2
        cleaned_expansion = filter_noise_morphology(expansion_mask)

        pixel_ha = (resolution_m * resolution_m) / 10000.0
        initial_builtup_ha = round(float(np.count_nonzero(builtup_t1)) * pixel_ha, 2)
        total_builtup_t2_ha = round(float(np.count_nonzero(builtup_t2)) * pixel_ha, 2)
        new_expansion_ha = round(float(np.count_nonzero(cleaned_expansion)) * pixel_ha, 2)
        growth_rate_pct = round((new_expansion_ha / max(initial_builtup_ha, 1.0)) * 100.0, 2)

        vector_anomalies = vectorize_binary_mask_to_geojson(
            cleaned_expansion,
            bbox=bbox,
            min_area_ha=0.20,
            resolution_m=resolution_m,
            module_label="New Impervious Surface Candidate"
        )

        return {
            "module": "urbanwatch",
            "metrics": {
                "initial_builtup_extent_ha": initial_builtup_ha,
                "current_builtup_extent_ha": total_builtup_t2_ha,
                "new_impervious_expansion_ha": new_expansion_ha,
                "expansion_growth_rate_pct": growth_rate_pct,
                "cautious_assessment": (
                    f"Identified {new_expansion_ha} ha of new impervious surface expansion (+{growth_rate_pct}% growth). "
                    "Planning authority verification advised to ascertain zoning compliance and setback adherence."
                )
            },
            "total_change_ha": new_expansion_ha,
            "vector_geojson": vector_anomalies
        }
