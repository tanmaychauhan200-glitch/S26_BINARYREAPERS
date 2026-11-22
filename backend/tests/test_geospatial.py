import numpy as np
import pytest
from backend.app.geospatial.crs import get_utm_epsg_for_lon_lat, calculate_polygon_area_ha
from backend.app.geospatial.cloud_mask import create_scl_valid_mask, SCL_CLOUD_HIGH, SCL_VEGETATION
from backend.app.geospatial.vectorizer import vectorize_binary_mask_to_geojson

def test_utm_zone_determination():
    # Delhi (~77.2°E) -> Zone 43N
    assert get_utm_epsg_for_lon_lat(77.2, 28.6) == 32643
    # Bengaluru (~77.6°E) -> Zone 43N / 44N
    assert get_utm_epsg_for_lon_lat(77.6, 12.9) == 32643
    # Assam / Guwahati (~91.7°E) -> Zone 46N
    assert get_utm_epsg_for_lon_lat(91.7, 26.1) == 32646

def test_polygon_area_calculation():
    # 1km x 1km square in Delhi = 100 hectares
    # ~0.009 degrees latitude is roughly 1km
    geom = {
        "type": "Polygon",
        "coordinates": [[
            [77.200, 28.500],
            [77.210, 28.500],
            [77.210, 28.509],
            [77.200, 28.509],
            [77.200, 28.500]
        ]]
    }
    area_ha = calculate_polygon_area_ha(geom)
    assert 90.0 <= area_ha <= 110.0

def test_scl_cloud_masking():
    # 10x10 synthetic raster with 20 cloud pixels and 80 vegetation pixels
    scl = np.full((10, 10), SCL_VEGETATION, dtype=np.uint8)
    scl[0:2, :] = SCL_CLOUD_HIGH  # 20 pixels
    mask, valid_pct = create_scl_valid_mask(scl)
    assert valid_pct == 80.0
    assert not mask[0, 0]
    assert mask[5, 5]

def test_vectorizer_clustering():
    # 20x20 binary mask with a 6x6 changed patch
    mask = np.zeros((20, 20), dtype=bool)
    mask[5:11, 5:11] = True # 36 pixels; morphological cross filter erodes 4 corner pixels -> 32 pixels * 0.01 ha = 0.32 ha
    bbox = [77.20, 28.50, 77.22, 28.52]
    geojson = vectorize_binary_mask_to_geojson(mask, bbox, min_area_ha=0.1, resolution_m=10.0)
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) == 1
    assert geojson["features"][0]["properties"]["area_ha"] == 0.32
