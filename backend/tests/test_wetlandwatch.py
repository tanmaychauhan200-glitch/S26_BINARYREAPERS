import numpy as np
import pytest
from backend.app.modules.wetlandwatch.processor import WetlandWatchProcessor

def test_wetlandwatch_processing():
    proc = WetlandWatchProcessor()
    shape = (20, 20)
    # T1: entire 10x10 center is inundated wetland
    t1_bands = {
        'green': np.full(shape, 0.15, dtype=np.float32),
        'swir': np.full(shape, 0.35, dtype=np.float32),
    }
    t1_bands['green'][5:15, 5:15] = 0.45
    t1_bands['swir'][5:15, 5:15] = 0.05

    # T2: water contracted to 5x5 center (shrinkage around perimeter)
    t2_bands = {
        'green': np.full(shape, 0.15, dtype=np.float32),
        'swir': np.full(shape, 0.35, dtype=np.float32),
    }
    t2_bands['green'][7:12, 7:12] = 0.45
    t2_bands['swir'][7:12, 7:12] = 0.05

    bbox = [91.64, 26.11, 91.68, 26.15]
    res = proc.process(t1_bands, t2_bands, bbox, resolution_m=10.0)

    assert res["module"] == "wetlandwatch"
    assert res["metrics"]["permanent_water_core_ha"] == 0.25 # 25 pixels * 0.01 ha
    assert res["metrics"]["seasonal_water_loss_ha"] == 0.75 # 75 pixels * 0.01 ha
    assert res["total_change_ha"] == 0.75
