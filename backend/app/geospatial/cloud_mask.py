import numpy as np
from typing import Tuple

# Sentinel-2 Scene Classification Layer (SCL) Class Constants
SCL_NO_DATA = 0
SCL_SATURATED = 1
SCL_DARK_FEATURES = 2
SCL_CLOUD_SHADOW = 3
SCL_VEGETATION = 4
SCL_NOT_VEGETATED = 5
SCL_WATER = 6
SCL_UNCLASSIFIED = 7
SCL_CLOUD_MEDIUM = 8
SCL_CLOUD_HIGH = 9
SCL_THIN_CIRRUS = 10
SCL_SNOW_ICE = 11

def create_scl_valid_mask(scl_raster: np.ndarray) -> Tuple[np.ndarray, float]:
    """
    Creates a boolean mask (True = Clear / Valid pixel, False = Obscured/Invalid)
    from Sentinel-2 L2A Scene Classification Layer (SCL).
    
    Masks out:
    - 0: No Data
    - 3: Cloud Shadows
    - 8: Cloud Medium Probability
    - 9: Cloud High Probability
    - 10: Thin Cirrus
    
    Returns:
    (valid_boolean_mask, valid_pixel_percentage)
    """
    invalid_classes = [SCL_NO_DATA, SCL_CLOUD_SHADOW, SCL_CLOUD_MEDIUM, SCL_CLOUD_HIGH, SCL_THIN_CIRRUS]
    
    # Initialize valid mask as True
    valid_mask = np.isin(scl_raster, invalid_classes, invert=True)
    
    total_pixels = scl_raster.size
    valid_pixels = int(np.count_nonzero(valid_mask))
    valid_pct = round((valid_pixels / total_pixels) * 100.0, 2) if total_pixels > 0 else 0.0
    
    return valid_mask, valid_pct

def apply_cloud_mask(raster_band: np.ndarray, valid_mask: np.ndarray, fill_value: float = -9999.0) -> np.ndarray:
    """Replaces obscured or cloud-shadow pixels with fill_value."""
    masked = raster_band.copy().astype(np.float32)
    masked[~valid_mask] = fill_value
    return masked
