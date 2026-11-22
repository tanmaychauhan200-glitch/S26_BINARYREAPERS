import numpy as np
import pytest
from backend.app.modules.forestguard.processor import ForestGuardProcessor

def test_forestguard_disturbance():
    proc = ForestGuardProcessor()
    shape = (20, 20)
    # T1: dense forest canopy across whole raster (NIR=0.75, Red=0.08, NDVI ~ 0.80)
    t1_bands = {
        'nir': np.full(shape, 0.75, dtype=np.float32),
        'red': np.full(shape, 0.08, dtype=np.float32),
    }

    # T2: 6x6 patch in center disturbed / cleared (NIR=0.25, Red=0.20, NDVI ~ 0.11)
    t2_bands = {
        'nir': np.full(shape, 0.75, dtype=np.float32),
        'red': np.full(shape, 0.08, dtype=np.float32),
    }
    t2_bands['nir'][6:12, 6:12] = 0.25
    t2_bands['red'][6:12, 6:12] = 0.20

    bbox = [76.40, 11.03, 76.45, 11.08]
    res = proc.process(t1_bands, t2_bands, bbox, resolution_m=10.0)

    assert res["module"] == "forestguard"
    assert res["metrics"]["potential_canopy_disturbance_ha"] > 0
    assert "canopy_patch_count" in res["metrics"]
    assert "cautious_assessment" in res["metrics"]
