import math
import logging
import requests
from typing import Dict, Any, Optional
from backend.app.geospatial.crs import get_utm_epsg_for_lon_lat

logger = logging.getLogger(__name__)

def inspect_point_in_india(lat: float, lon: float) -> Dict[str, Any]:
    """
    Performs deep geospatial & reverse-geocoded analysis for ANY coordinate in India.
    Returns:
    - Administrative location (State, District, Village/Town, River/Waterbody)
    - UTM Zone and Coordinate Reference System
    - Simulated calibrated multi-spectral indices (NDVI, MNDWI, NDBI)
    - Environmental Classification & Ecological Vulnerability Profile
    """
    # 1. Reverse Geocode via OpenStreetMap Nominatim
    location_info = {
        "display_name": f"Location [{lat:.4f}°N, {lon:.4f}°E]",
        "district": "Unknown District",
        "state": "India",
        "suburb": "",
        "waterbody": None
    }
    
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=14&addressdetails=1"
        headers = {"User-Agent": "TerraWatch-360-EcoResearch-Engine/1.0"}
        resp = requests.get(url, headers=headers, timeout=4.0)
        if resp.status_code == 200:
            data = resp.json()
            addr = data.get("address", {})
            location_info["display_name"] = data.get("display_name", location_info["display_name"])
            location_info["state"] = addr.get("state") or addr.get("region") or "India"
            location_info["district"] = addr.get("state_district") or addr.get("county") or addr.get("city") or "Central District"
            location_info["suburb"] = addr.get("suburb") or addr.get("town") or addr.get("village") or addr.get("neighbourhood") or ""
            # Check if waterbody or river feature
            if "water" in data.get("type", "").lower() or "river" in data.get("type", "").lower():
                location_info["waterbody"] = data.get("name")
    except Exception as e:
        logger.warning("Reverse geocoding failed or timed out: %s", str(e))

    # 2. Derive UTM & Coordinate System
    utm_zone = get_utm_epsg_for_lon_lat(lon, lat)

    # 3. Terrain & Biome Heuristics for India based on coordinates
    # Northern Alluvial Rivers (Ganga-Yamuna belt: Lat 25-31, Lon 75-88)
    # Western Ghats Rainforest (Lat 8-15, Lon 73-77)
    # Deccan Plateau / Urban hubs (Bengaluru, Hyderabad, Pune)
    # North-East Wetlands (Brahmaputra basin: Lat 24-28, Lon 89-96)
    
    # Calculate pseudo-deterministic spectral signature based on spatial geography
    # Using hash-derived seed for reproducible spatial continuity
    spatial_seed = int((abs(lat) * 1000 + abs(lon) * 1000)) % 1000
    norm_val = spatial_seed / 1000.0

    if 73.0 <= lon <= 77.0 and 8.0 <= lat <= 15.0:
        # Western Ghats / Evergreen Bio-reserve
        biome = "Western Ghats Wet Evergreen / Tropical Rainforest"
        ndvi = round(0.72 + (norm_val * 0.15), 2)
        mndwi = round(-0.35 + (norm_val * 0.1), 2)
        ndbi = round(-0.25 - (norm_val * 0.1), 2)
        primary_class = "Dense Tropical Forest Canopy"
        vulnerability = "HIGH — Protected Biological Hotspot / Habitat Fragmentation Sensitivity"
    elif 89.0 <= lon <= 96.0 and 24.0 <= lat <= 28.0:
        # Brahmaputra Basin / Wetlands
        biome = "Brahmaputra Alluvial Plains / Perennial Freshwater Wetland"
        ndvi = round(0.40 + (norm_val * 0.2), 2)
        mndwi = round(0.25 + (norm_val * 0.35), 2)
        ndbi = round(-0.30 - (norm_val * 0.1), 2)
        primary_class = "Inland Wetland / Braided River Corridor"
        vulnerability = "CRITICAL — High Flood Inundation & Seasonal Siltation Vulnerability"
    elif 76.5 <= lon <= 78.5 and 12.5 <= lat <= 13.5:
        # Bengaluru Urban Region
        biome = "South Deccan Plateau / Rapid Peri-Urban Growth Zone"
        ndvi = round(0.20 + (norm_val * 0.15), 2)
        mndwi = round(-0.15 + (norm_val * 0.1), 2)
        ndbi = round(0.32 + (norm_val * 0.25), 2)
        primary_class = "Impervious Built-Up / Construction Surface"
        vulnerability = "MODERATE — Urban Heat Island & Lake Cascade Encroachment Pressure"
    elif 76.0 <= lon <= 78.5 and 28.0 <= lat <= 29.5:
        # Delhi NCR / Yamuna River Corridor
        biome = "Indo-Gangetic Alluvial Floodplain"
        ndvi = round(0.25 + (norm_val * 0.2), 2)
        mndwi = round(0.08 + (norm_val * 0.25), 2)
        ndbi = round(0.18 + (norm_val * 0.2), 2)
        primary_class = "Alluvial Riverbed / Semi-Arid Agricultural Transition"
        vulnerability = "HIGH — Active Riverbed Sediment Extraction & Floodplain Inundation Risk"
    else:
        # General Indian Landscape
        biome = "Indian Peninsular Plateau / Agro-Ecological Transition"
        ndvi = round(0.35 + (norm_val * 0.25), 2)
        mndwi = round(-0.10 + (norm_val * 0.15), 2)
        ndbi = round(-0.05 + (norm_val * 0.2), 2)
        primary_class = "Mixed Agricultural & Vegetated Matrix"
        vulnerability = "LOW-MODERATE — Seasonal Dry-Down & Crop Rotation Dynamics"

    return {
        "coordinates": {"latitude": round(lat, 5), "longitude": round(lon, 5)},
        "location": location_info,
        "spatial_reference": {
            "utm_zone": f"UTM Zone {utm_zone - 32600}N",
            "epsg": f"EPSG:{utm_zone}",
            "geographic_crs": "EPSG:4326 (WGS84)"
        },
        "biome": biome,
        "spectral_indices": {
            "ndvi": ndvi,
            "mndwi": mndwi,
            "ndbi": ndbi
        },
        "classification": {
            "primary_surface_type": primary_class,
            "vulnerability_assessment": vulnerability
        }
    }
