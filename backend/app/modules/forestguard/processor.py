import numpy as np
from typing import Dict, Any, List
from scipy.ndimage import label
from backend.app.geospatial.indices import compute_ndvi, compute_differenced_index
from backend.app.geospatial.vectorizer import vectorize_binary_mask_to_geojson, filter_noise_morphology

class ForestGuardProcessor:
    """
    Module 3: ForestGuard
    Monitors forest canopy cover, spectral canopy disturbances,
    and landscape fragmentation patterns across protected bio-reserves.
    """

    def __init__(self, canopy_ndvi_thresh: float = 0.60, disturbance_dndvi_thresh: float = 0.20):
        self.canopy_ndvi_thresh = canopy_ndvi_thresh
        self.disturbance_dndvi_thresh = disturbance_dndvi_thresh

    def process(
        self,
        t1_bands: Dict[str, np.ndarray],
        t2_bands: Dict[str, np.ndarray],
        bbox: List[float],
        resolution_m: float = 10.0
    ) -> Dict[str, Any]:
        ndvi_t1 = compute_ndvi(t1_bands['nir'], t1_bands['red'])
        ndvi_t2 = compute_ndvi(t2_bands['nir'], t2_bands['red'])

        # Baseline canopy mask
        dense_canopy_t1 = ndvi_t1 >= self.canopy_ndvi_thresh
        dense_canopy_t2 = ndvi_t2 >= self.canopy_ndvi_thresh

        # dNDVI differencing
        dndvi = compute_differenced_index(ndvi_t1, ndvi_t2)

        # Disturbance: Was canopy in T1, and dNDVI drops significantly
        disturbance_mask = dense_canopy_t1 & (dndvi >= self.disturbance_dndvi_thresh)
        cleaned_disturbance = filter_noise_morphology(disturbance_mask)

        # Regrowth / Recovery: dNDVI <= -0.20
        regrowth_mask = (~dense_canopy_t1) & (dndvi <= -0.20)

        # Landscape Fragmentation Metrics (Fragstats concept)
        cleaned_canopy_t2 = filter_noise_morphology(dense_canopy_t2)
        _, num_patches = label(cleaned_canopy_t2)

        pixel_ha = (resolution_m * resolution_m) / 10000.0
        canopy_area_ha = round(float(np.count_nonzero(dense_canopy_t2)) * pixel_ha, 2)
        disturbance_ha = round(float(np.count_nonzero(cleaned_disturbance)) * pixel_ha, 2)
        regrowth_ha = round(float(np.count_nonzero(regrowth_mask)) * pixel_ha, 2)
        mean_patch_size_ha = round(canopy_area_ha / max(num_patches, 1), 2)

        vector_anomalies = vectorize_binary_mask_to_geojson(
            cleaned_disturbance,
            bbox=bbox,
            min_area_ha=0.20,
            resolution_m=resolution_m,
            module_label="Potential Canopy Disturbance Alert"
        )

        return {
            "module": "forestguard",
            "metrics": {
                "standing_canopy_area_ha": canopy_area_ha,
                "potential_canopy_disturbance_ha": disturbance_ha,
                "vegetation_regrowth_gain_ha": regrowth_ha,
                "canopy_patch_count": num_patches,
                "mean_patch_size_ha": mean_patch_size_ha,
                "cautious_assessment": (
                    f"Identified {disturbance_ha} ha of spectral canopy disturbance across {len(vector_anomalies['features'])} patches. "
                    "Field verification required to distinguish seasonal leaf shedding or selective thinning from deforestation."
                )
            },
            "total_change_ha": disturbance_ha,
            "vector_geojson": vector_anomalies
        }
