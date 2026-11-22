import numpy as np
from typing import Dict, Any, List
from scipy.ndimage import binary_opening, binary_closing, label

def filter_noise_morphology(binary_mask: np.ndarray, iterations: int = 1) -> np.ndarray:
    """
    Applies morphological opening (erosion followed by dilation)
    to eliminate isolated single-pixel false alarms, then closing to fill micro-holes.
    """
    struct = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ], dtype=bool)
    
    opened = binary_opening(binary_mask, structure=struct, iterations=iterations)
    closed = binary_closing(opened, structure=struct, iterations=iterations)
    return closed

def vectorize_binary_mask_to_geojson(
    binary_mask: np.ndarray,
    bbox: List[float],
    min_area_ha: float = 0.25,
    resolution_m: float = 10.0,
    module_label: str = "Detected Change"
) -> Dict[str, Any]:
    """
    Clusters contiguous changed pixels into vector polygons, transforms them to
    geographic GeoJSON coordinates [min_lon, min_lat, max_lon, max_lat],
    and computes planar area in hectares.
    """
    cleaned_mask = filter_noise_morphology(binary_mask)
    labeled_array, num_features = label(cleaned_mask)
    
    height, width = binary_mask.shape
    min_lon, min_lat, max_lon, max_lat = bbox
    pixel_width_deg = (max_lon - min_lon) / max(width, 1)
    pixel_height_deg = (max_lat - min_lat) / max(height, 1)
    
    # 1 pixel at resolution_m x resolution_m in hectares
    pixel_area_ha = (resolution_m * resolution_m) / 10000.0
    
    features = []
    for feat_idx in range(1, num_features + 1):
        pixel_indices = np.argwhere(labeled_array == feat_idx)
        pixel_count = len(pixel_indices)
        feat_area_ha = round(pixel_count * pixel_area_ha, 2)
        
        if feat_area_ha < min_area_ha:
            continue
            
        # Compute bounding rectangle polygon for the cluster
        min_r = int(np.min(pixel_indices[:, 0]))
        max_r = int(np.max(pixel_indices[:, 0]))
        min_c = int(np.min(pixel_indices[:, 1]))
        max_c = int(np.max(pixel_indices[:, 1]))
        
        poly_min_lon = round(min_lon + (min_c * pixel_width_deg), 6)
        poly_max_lon = round(min_lon + ((max_c + 1) * pixel_width_deg), 6)
        poly_max_lat = round(max_lat - (min_r * pixel_height_deg), 6)
        poly_min_lat = round(max_lat - ((max_r + 1) * pixel_height_deg), 6)
        
        polygon_coords = [
            [poly_min_lon, poly_min_lat],
            [poly_max_lon, poly_min_lat],
            [poly_max_lon, poly_max_lat],
            [poly_min_lon, poly_max_lat],
            [poly_min_lon, poly_min_lat]
        ]
        
        features.append({
            "type": "Feature",
            "properties": {
                "feature_id": f"poly_{feat_idx}",
                "label": module_label,
                "area_ha": feat_area_ha,
                "pixel_count": pixel_count,
                "confidence": 0.85
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [polygon_coords]
            }
        })
        
    return {
        "type": "FeatureCollection",
        "features": features
    }
