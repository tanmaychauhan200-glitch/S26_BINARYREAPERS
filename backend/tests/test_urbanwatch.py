import numpy as np
import pytest
from backend.app.modules.urbanwatch.processor import UrbanWatchProcessor

def test_urbanwatch_expansion():
    proc = UrbanWatchProcessor()
    shape = (20, 20)
    # T1: mostly vegetation (NIR=0.6, Red=0.1, SWIR=0.2, Green=0.2)
    t1_bands = {
        'swir': np.full(shape, 0.20, dtype=np.float32),
        'nir': np.full(shape, 0.60, dtype=np.float32),
        'red': np.full(shape, 0.10, dtype=np.float32),
        'green': np.full(shape, 0.20, dtype=np.float32)
    }

    # T2: 6x6 patch converted to built-up impervious concrete (SWIR=0.55, NIR=0.25, Red=0.35, Green=0.25)
    t2_bands = {
        'swir': np.full(shape, 0.20, dtype=np.float32),
        'nir': np.full(shape, 0.60, dtype=np.float32),
        'red': np.full(shape, 0.10, dtype=np.float32),
        'green': np.full(shape, 0.20, dtype=np.float32)
    }
    t2_bands['swir'][7:13, 7:13] = 0.55
    t2_bands['nir'][7:13, 7:13] = 0.25
    t2_bands['red'][7:13, 7:13] = 0.35
    t2_bands['green'][7:13, 7:13] = 0.25

    bbox = [77.70, 12.89, 77.75, 12.94]
    res = proc.process(t1_bands, t2_bands, bbox, resolution_m=10.0)

    assert res["module"] == "urbanwatch"
    assert res["metrics"]["new_impervious_expansion_ha"] > 0
    assert "expansion_growth_rate_pct" in res["metrics"]
    assert "cautious_assessment" in res["metrics"]
