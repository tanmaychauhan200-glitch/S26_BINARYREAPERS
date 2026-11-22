import math
from typing import List, Tuple
from pyproj import Transformer, CRS

def get_utm_epsg_for_lon_lat(lon: float, lat: float) -> int:
    """
    Computes the appropriate Indian UTM EPSG code (Northern hemisphere)
    Zone 43N: 72°E - 78°E (EPSG:32643 - Delhi, Mumbai, Gujarat, Rajasthan, Western Ghats)
    Zone 44N: 78°E - 84°E (EPSG:32644 - Hyderabad, Bengaluru, UP, MP)
    Zone 45N: 84°E - 90°E (EPSG:32645 - Odisha, West Bengal, Bihar, Chhattisgarh)
    Zone 46N: 90°E - 96°E (EPSG:32646 - Assam, Deepor Beel, Northeast India)
    """
    zone_number = int(math.floor((lon + 180) / 6) + 1)
    return 32600 + zone_number

def transform_coordinates(
    coords: List[Tuple[float, float]],
    from_epsg: int = 4326,
    to_epsg: int = 32643
) -> List[Tuple[float, float]]:
    """Transform list of (x, y) / (lon, lat) points between CRS systems."""
    transformer = Transformer.from_crs(f"EPSG:{from_epsg}", f"EPSG:{to_epsg}", always_xy=True)
    return [transformer.transform(x, y) for x, y in coords]

def calculate_polygon_area_ha(geometry_geojson: dict) -> float:
    """
    Computes accurate planar surface area in hectares by projecting
    the GeoJSON polygon to the optimal local UTM zone.
    Prevents erroneous degree-pixel area calculations.
    """
    coords = geometry_geojson.get("coordinates", [[]])[0]
    if len(coords) < 3:
        return 0.0

    # Auto-detect central UTM zone from polygon centroid
    center_lon = sum(pt[0] for pt in coords) / len(coords)
    center_lat = sum(pt[1] for pt in coords) / len(coords)
    utm_epsg = get_utm_epsg_for_lon_lat(center_lon, center_lat)

    transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{utm_epsg}", always_xy=True)
    projected_pts = [transformer.transform(pt[0], pt[1]) for pt in coords]

    # Shoelace formula on UTM meter coordinates
    n = len(projected_pts)
    area_sq_m = 0.0
    for i in range(n):
        j = (i + 1) % n
        area_sq_m += projected_pts[i][0] * projected_pts[j][1]
        area_sq_m -= projected_pts[j][0] * projected_pts[i][1]
    area_sq_m = abs(area_sq_m) / 2.0

    # 1 hectare = 10,000 square meters
    return round(area_sq_m / 10000.0, 2)
