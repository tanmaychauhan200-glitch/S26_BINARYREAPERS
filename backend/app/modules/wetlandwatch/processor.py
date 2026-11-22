import numpy as np
from typing import Dict, Any, List
from backend.app.geospatial.indices import compute_mndwi
from backend.app.geospatial.vectorizer import vectorize_binary_mask_to_geojson

class WetlandWatchProcessor:
    """
    Module 2: WetlandWatch
    Monitors wetland waterbody persistence, seasonal water contraction,
    and ecological buffer shrinkage across Indian Ramsar and inland water bodies.
    """

    def __init__(self, water_thresh: float = 0.05):
        self.water_thresh = water_thresh

    def process(
        self,
        t1_bands: Dict[str, np.ndarray],
        t2_bands: Dict[str, np.ndarray],
        bbox: List[float],
        resolution_m: float = 10.0
    ) -> Dict[str, Any]:
        mndwi_t1 = compute_mndwi(t1_bands['green'], t1_bands['swir'])
        mndwi_t2 = compute_mndwi(t2_bands['green'], t2_bands['swir'])

        water_t1 = mndwi_t1 > self.water_thresh
        water_t2 = mndwi_t2 > self.water_thresh

        # Permanent water: Present in both observations
        permanent_water = water_t1 & water_t2

        # Seasonal water loss / shrinkage: Present in T1 but dry in T2
        water_loss_mask = water_t1 & (~water_t2)

        # Seasonal water expansion: Dry in T1 but inundated in T2
        water_gain_mask = (~water_t1) & water_t2

        pixel_ha = (resolution_m * resolution_m) / 10000.0
        permanent_water_ha = round(float(np.count_nonzero(permanent_water)) * pixel_ha, 2)
        water_loss_ha = round(float(np.count_nonzero(water_loss_mask)) * pixel_ha, 2)
        water_gain_ha = round(float(np.count_nonzero(water_gain_mask)) * pixel_ha, 2)
        current_water_ha = round(float(np.count_nonzero(water_t2)) * pixel_ha, 2)

        vector_anomalies = vectorize_binary_mask_to_geojson(
            water_loss_mask,
            bbox=bbox,
            min_area_ha=0.25,
            resolution_m=resolution_m,
            module_label="Seasonal Water Contraction / Shrinkage"
        )

        return {
            "module": "wetlandwatch",
            "metrics": {
                "current_water_extent_ha": current_water_ha,
                "permanent_water_core_ha": permanent_water_ha,
                "seasonal_water_loss_ha": water_loss_ha,
                "seasonal_water_gain_ha": water_gain_ha,
                "cautious_assessment": (
                    f"Waterbody contracted by {water_loss_ha} ha relative to baseline. "
                    "Consistent with normal post-monsoon dry-down unless persistent across multi-year baselines."
                )
            },
            "total_change_ha": water_loss_ha,
            "vector_geojson": vector_anomalies
        }
