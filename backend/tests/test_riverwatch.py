import numpy as np
import pytest
from backend.app.modules.riverwatch.processor import RiverWatchProcessor

def test_riverwatch_processing():
    proc = RiverWatchProcessor()
    # 20x20 test grids
    shape = (20, 20)
    # T1: water in center column 10
    t1_bands = {
        'green': np.full(shape, 0.15, dtype=np.float32),
        'red': np.full(shape, 0.10, dtype=np.float32),
        'nir': np.full(shape, 0.50, dtype=np.float32),
        'swir': np.full(shape, 0.30, dtype=np.float32),
    }
    t1_bands['green'][:, 10] = 0.40 # Water channel
    t1_bands['swir'][:, 10] = 0.05
    t1_bands['nir'][:, 10] = 0.05

    # T2: water shifted to column 11 (bank retreat along col 11)
    t2_bands = {
        'green': np.full(shape, 0.15, dtype=np.float32),
        'red': np.full(shape, 0.10, dtype=np.float32),
        'nir': np.full(shape, 0.50, dtype=np.float32),
        'swir': np.full(shape, 0.30, dtype=np.float32),
    }
    t2_bands['green'][:, 11] = 0.40
    t2_bands['swir'][:, 11] = 0.05
    t2_bands['nir'][:, 11] = 0.05

    bbox = [77.20, 28.50, 77.22, 28.52]
    res = proc.process(t1_bands, t2_bands, bbox, resolution_m=10.0)

    assert res["module"] == "riverwatch"
    assert "metrics" in res
    assert res["metrics"]["bank_retreat_area_ha"] > 0
    assert "cautious_assessment" in res["metrics"]
