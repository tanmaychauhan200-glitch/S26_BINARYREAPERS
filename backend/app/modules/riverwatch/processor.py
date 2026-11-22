import numpy as np
from typing import Dict, Any, List
from backend.app.geospatial.indices import compute_mndwi, compute_ndvi
from backend.app.geospatial.vectorizer import vectorize_binary_mask_to_geojson

class RiverWatchProcessor:
    """
    Module 1: RiverWatch
    Monitors active river channels, riverbank migration/retreat,
    and exposed sediment/sandbar extraction dynamics.
    """

    def __init__(self, water_mndwi_thresh: float = 0.05, sandbar_ndvi_thresh: float = 0.25):
        self.water_mndwi_thresh = water_mndwi_thresh
        self.sandbar_ndvi_thresh = sandbar_ndvi_thresh

    def process(
        self,
        t1_bands: Dict[str, np.ndarray], # 'green', 'red', 'nir', 'swir'
        t2_bands: Dict[str, np.ndarray],
        bbox: List[float],
        resolution_m: float = 10.0
    ) -> Dict[str, Any]:
        # 1. Delineate water bodies for T1 and T2 using MNDWI
        mndwi_t1 = compute_mndwi(t1_bands['green'], t1_bands['swir'])
        mndwi_t2 = compute_mndwi(t2_bands['green'], t2_bands['swir'])
        
        water_t1 = mndwi_t1 > self.water_mndwi_thresh
        water_t2 = mndwi_t2 > self.water_mndwi_thresh

        # 2. Exposed sediment/sandbars: low NDVI, negative MNDWI, elevated Red reflectance
        ndvi_t2 = compute_ndvi(t2_bands['nir'], t2_bands['red'])
        sandbar_t2 = (
            (ndvi_t2 < self.sandbar_ndvi_thresh) & 
            (mndwi_t2 < 0.0) & 
            (t2_bands['red'] > 0.12) &
            (~water_t2)
        )

        # 3. Detect Channel Migration / Riverbank Retreat:
        # Areas that were land in T1 but are now water in T2 (bank erosion/retreat)
        bank_retreat_mask = (~water_t1) & water_t2

        # 4. Detect Exposed Sediment Change:
        ndvi_t1 = compute_ndvi(t1_bands['nir'], t1_bands['red'])
        sandbar_t1 = (
            (ndvi_t1 < self.sandbar_ndvi_thresh) & 
            (mndwi_t1 < 0.0) & 
            (t1_bands['red'] > 0.12) &
            (~water_t1)
        )
        sediment_shift_mask = (~sandbar_t1) & sandbar_t2

        # 5. Compute planar surface areas (ha)
        pixel_ha = (resolution_m * resolution_m) / 10000.0
        water_area_t2_ha = round(float(np.count_nonzero(water_t2)) * pixel_ha, 2)
        sandbar_area_t2_ha = round(float(np.count_nonzero(sandbar_t2)) * pixel_ha, 2)
        bank_retreat_ha = round(float(np.count_nonzero(bank_retreat_mask)) * pixel_ha, 2)
        sediment_shift_ha = round(float(np.count_nonzero(sediment_shift_mask)) * pixel_ha, 2)

        # 6. Vectorize anomalies for interactive map rendering
        vector_anomalies = vectorize_binary_mask_to_geojson(
            sediment_shift_mask,
            bbox=bbox,
            min_area_ha=0.20,
            resolution_m=resolution_m,
            module_label="Unusual Riverbed Exposed Sediment Shift"
        )

        return {
            "module": "riverwatch",
            "metrics": {
                "active_water_area_ha": water_area_t2_ha,
                "exposed_sandbar_area_ha": sandbar_area_t2_ha,
                "bank_retreat_area_ha": bank_retreat_ha,
                "exposed_sediment_increase_ha": sediment_shift_ha,
                "cautious_assessment": (
                    f"Exposed sediment shift of {sediment_shift_ha} ha and riverbank retreat of "
                    f"{bank_retreat_ha} ha detected. Requires field investigation before drawing extraction inferences."
                )
            },
            "total_change_ha": round(sediment_shift_ha + bank_retreat_ha, 2),
            "vector_geojson": vector_anomalies
        }
