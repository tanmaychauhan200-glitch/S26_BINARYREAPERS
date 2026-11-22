import numpy as np
import pytest
from backend.app.geospatial.indices import (
    compute_ndwi,
    compute_mndwi,
    compute_ndvi,
    compute_ndbi,
    compute_differenced_index
)

def test_ndwi_water_detection():
    # Pure water: high green (0.4), very low NIR (0.05)
    green = np.array([[0.40]], dtype=np.float32)
    nir = np.array([[0.05]], dtype=np.float32)
    ndwi = compute_ndwi(green, nir)
    assert ndwi[0, 0] > 0.5
    # Vegetated land: low green (0.1), high NIR (0.6)
    green_veg = np.array([[0.10]], dtype=np.float32)
    nir_veg = np.array([[0.60]], dtype=np.float32)
    ndwi_veg = compute_ndwi(green_veg, nir_veg)
    assert ndwi_veg[0, 0] < 0.0

def test_ndvi_canopy_detection():
    # Dense forest canopy: high NIR (0.7), low Red (0.08)
    nir = np.array([[0.70]], dtype=np.float32)
    red = np.array([[0.08]], dtype=np.float32)
    ndvi = compute_ndvi(nir, red)
    assert ndvi[0, 0] > 0.70
    # Degraded/bare ground: low NIR (0.2), moderate Red (0.2)
    nir_bare = np.array([[0.20]], dtype=np.float32)
    red_bare = np.array([[0.20]], dtype=np.float32)
    ndvi_bare = compute_ndvi(nir_bare, red_bare)
    assert abs(ndvi_bare[0, 0]) < 0.05

def test_zero_denominator_safe():
    # Zero in both bands
    band_a = np.array([[0.0]], dtype=np.float32)
    band_b = np.array([[0.0]], dtype=np.float32)
    res = compute_ndwi(band_a, band_b)
    assert res[0, 0] == -9999.0

def test_differenced_index():
    t1 = np.array([[0.80, 0.40]], dtype=np.float32)
    t2 = np.array([[0.30, 0.40]], dtype=np.float32)
    diff = compute_differenced_index(t1, t2)
    assert pytest.approx(diff[0, 0], 0.01) == 0.50
    assert pytest.approx(diff[0, 1], 0.01) == 0.00
