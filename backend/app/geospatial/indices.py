import numpy as np

def compute_normalized_difference(
    band_a: np.ndarray,
    band_b: np.ndarray,
    nodata_val: float = -9999.0
) -> np.ndarray:
    """
    Computes generic normalized difference: (band_a - band_b) / (band_a + band_b).
    Handles zero division, negative denominator artifacts, and invalid input values.
    """
    a = band_a.astype(np.float32)
    b = band_b.astype(np.float32)
    
    denominator = a + b
    numerator = a - b
    
    with np.errstate(divide='ignore', invalid='ignore'):
        result = np.where(
            (denominator != 0) & np.isfinite(denominator),
            numerator / denominator,
            nodata_val
        )
    # Clip valid values strictly to [-1.0, 1.0]
    valid_mask = result != nodata_val
    result[valid_mask] = np.clip(result[valid_mask], -1.0, 1.0)
    return result

def compute_ndwi(green: np.ndarray, nir: np.ndarray) -> np.ndarray:
    """
    Normalized Difference Water Index (NDWI) — McFeeters (1996)
    Formula: (Green - NIR) / (Green + NIR)
    Sentinel-2: (B03 - B08) / (B03 + B08)
    Water features: NDWI > 0.0
    """
    return compute_normalized_difference(green, nir)

def compute_mndwi(green: np.ndarray, swir: np.ndarray) -> np.ndarray:
    """
    Modified Normalized Difference Water Index (MNDWI) — Xu (2006)
    Formula: (Green - SWIR) / (Green + SWIR)
    Sentinel-2: (B03 - B11) / (B03 + B11)
    Significantly suppresses built-up urban noise compared to NDWI.
    """
    return compute_normalized_difference(green, swir)

def compute_ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """
    Normalized Difference Vegetation Index (NDVI) — Rouse et al. (1974)
    Formula: (NIR - Red) / (NIR + Red)
    Sentinel-2: (B08 - B04) / (B08 + B04)
    Dense healthy forest: 0.6 - 0.9; Degraded canopy / scrub: 0.2 - 0.4
    """
    return compute_normalized_difference(nir, red)

def compute_ndbi(swir: np.ndarray, nir: np.ndarray) -> np.ndarray:
    """
    Normalized Difference Built-Up Index (NDBI) — Zha et al. (2003)
    Formula: (SWIR - NIR) / (SWIR + NIR)
    Sentinel-2: (B11 - B08) / (B11 + B08)
    Impervious surfaces & concrete: NDBI > 0.0
    """
    return compute_normalized_difference(swir, nir)

def compute_differenced_index(
    index_t1: np.ndarray,
    index_t2: np.ndarray,
    nodata_val: float = -9999.0
) -> np.ndarray:
    """
    Computes bi-temporal delta: Index(t1) - Index(t2).
    E.g., dNDVI > 0.20 indicates significant canopy loss / disturbance.
    """
    valid_mask = (index_t1 != nodata_val) & (index_t2 != nodata_val)
    delta = np.full_like(index_t1, nodata_val, dtype=np.float32)
    delta[valid_mask] = index_t1[valid_mask] - index_t2[valid_mask]
    return delta
