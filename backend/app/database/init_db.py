import logging
from backend.app.database.session import engine, Base, SessionLocal
from backend.app.models.study_area import StudyArea
from backend.app.models.satellite_scene import SatelliteScene
from datetime import date

logger = logging.getLogger(__name__)

# 16 Genuine Benchmark Study Areas across India (4 per module)
BENCHMARK_STUDY_AREAS = [
    # --- MODULE 1: RIVERWATCH ---
    {
        "id": "study_yamuna_delhi",
        "name": "Yamuna River (Delhi Reach)",
        "description": "Active braided river corridor and sediment extraction monitoring zone between Wazirabad and Okhla barrages.",
        "module_type": "riverwatch",
        "state": "National Capital Territory of Delhi",
        "area_ha": 3420.5,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [77.210, 28.710], [77.260, 28.710], [77.320, 28.530], [77.270, 28.530], [77.210, 28.710]
            ]]
        }
    },
    {
        "id": "study_ganga_haridwar",
        "name": "Ganga River (Haridwar Stretch)",
        "description": "Piedmont alluvial riverbed monitoring zone with high sediment transport and seasonal sandbar shifts.",
        "module_type": "riverwatch",
        "state": "Uttarakhand",
        "area_ha": 4850.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [78.120, 29.980], [78.200, 29.980], [78.230, 29.850], [78.140, 29.850], [78.120, 29.980]
            ]]
        }
    },
    {
        "id": "study_brahmaputra_guwahati",
        "name": "Brahmaputra River (Guwahati Reach)",
        "description": "Vast braided river system monitoring sediment island (char) dynamics, high-energy bank erosion, and channel migration.",
        "module_type": "riverwatch",
        "state": "Assam",
        "area_ha": 6200.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [91.680, 26.220], [91.820, 26.220], [91.820, 26.170], [91.680, 26.170], [91.680, 26.220]
            ]]
        }
    },
    {
        "id": "study_narmada_bharuch",
        "name": "Narmada River (Bharuch Estuary)",
        "description": "Lower tidal-alluvial reach monitoring seasonal sandbar exposure, estuarine sedimentation, and active channel shifts.",
        "module_type": "riverwatch",
        "state": "Gujarat",
        "area_ha": 5100.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [72.950, 21.750], [73.080, 21.750], [73.080, 21.660], [72.950, 21.660], [72.950, 21.750]
            ]]
        }
    },

    # --- MODULE 2: WETLANDWATCH ---
    {
        "id": "study_deepor_beel",
        "name": "Deepor Beel Ramsar Site",
        "description": "Major perennial freshwater wetland and Ramsar site facing seasonal shrinkage, water hyacinth proliferation, and drainage changes.",
        "module_type": "wetlandwatch",
        "state": "Assam",
        "area_ha": 4014.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [91.640, 26.110], [91.700, 26.110], [91.700, 26.155], [91.640, 26.155], [91.640, 26.110]
            ]]
        }
    },
    {
        "id": "study_chilika_north",
        "name": "Chilika Lake (Northern Sector)",
        "description": "Asia's largest brackish lagoon monitoring freshwater discharge channels, macrophyte dynamics, and seasonal boundary fluctuations.",
        "module_type": "wetlandwatch",
        "state": "Odisha",
        "area_ha": 8900.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [85.200, 19.700], [85.450, 19.700], [85.450, 19.850], [85.200, 19.850], [85.200, 19.700]
            ]]
        }
    },
    {
        "id": "study_keoladeo_ghana",
        "name": "Keoladeo Ghana Ramsar Wetland",
        "description": "Man-made and managed seasonal wetland sanctuary monitoring water persistence, inundation regimes, and dyke integrity.",
        "module_type": "wetlandwatch",
        "state": "Rajasthan",
        "area_ha": 2873.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [77.490, 27.140], [77.550, 27.140], [77.550, 27.200], [77.490, 27.200], [77.490, 27.140]
            ]]
        }
    },
    {
        "id": "study_vembanad_kol",
        "name": "Vembanad-Kol Wetland System",
        "description": "India's longest wetland lagoon monitoring agricultural barrier dynamics (Thanneermukkom bund) and surface water area variance.",
        "module_type": "wetlandwatch",
        "state": "Kerala",
        "area_ha": 7650.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [76.350, 9.550], [76.450, 9.550], [76.450, 9.700], [76.350, 9.700], [76.350, 9.550]
            ]]
        }
    },

    # --- MODULE 3: FORESTGUARD ---
    {
        "id": "study_silent_valley",
        "name": "Western Ghats (Silent Valley Buffer)",
        "description": "Continuous tropical wet evergreen rainforest canopy and global biodiversity hotspot monitoring spectral disturbances.",
        "module_type": "forestguard",
        "state": "Kerala",
        "area_ha": 8952.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [76.400, 11.030], [76.550, 11.030], [76.550, 11.160], [76.400, 11.160], [76.400, 11.030]
            ]]
        }
    },
    {
        "id": "study_hasdeo_arand",
        "name": "Hasdeo Arand Forest Corridor",
        "description": "Dense contiguous Sal forest canopy and elephant corridor monitoring vegetation loss, canopy gaps, and patch fragmentation.",
        "module_type": "forestguard",
        "state": "Chhattisgarh",
        "area_ha": 12400.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [82.600, 22.750], [82.850, 22.750], [82.850, 22.950], [82.600, 22.950], [82.600, 22.750]
            ]]
        }
    },
    {
        "id": "study_similipal_biosphere",
        "name": "Similipal Biosphere Reserve",
        "description": "UNESCO World Network of Biosphere Reserves monitoring semi-evergreen canopy integrity and fire disturbance scars.",
        "module_type": "forestguard",
        "state": "Odisha",
        "area_ha": 14200.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [86.250, 21.650], [86.500, 21.650], [86.500, 21.900], [86.250, 21.900], [86.250, 21.650]
            ]]
        }
    },
    {
        "id": "study_kaziranga_buffer",
        "name": "Kaziranga Buffer Forest Corridor",
        "description": "Mikir Hills and Karbi Anglong wildlife movement corridor monitoring canopy connectivity and seasonal phenological shifts.",
        "module_type": "forestguard",
        "state": "Assam",
        "area_ha": 9800.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [93.100, 26.500], [93.350, 26.500], [93.350, 26.650], [93.100, 26.650], [93.100, 26.500]
            ]]
        }
    },

    # --- MODULE 4: URBANWATCH ---
    {
        "id": "study_bengaluru_east",
        "name": "Bengaluru Peri-Urban Growth Corridor",
        "description": "Rapid built-up expansion corridor (Varthur/Sarjapur) analyzing conversion of agricultural plots and pressure on wetland cascades.",
        "module_type": "urbanwatch",
        "state": "Karnataka",
        "area_ha": 6500.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [77.700, 12.890], [77.790, 12.890], [77.790, 12.980], [77.700, 12.980], [77.700, 12.890]
            ]]
        }
    },
    {
        "id": "study_ncr_periurban",
        "name": "Delhi-NCR Peri-Urban Belt (Noida Ext.)",
        "description": "High-density concrete expansion monitoring in proximity to the Hindon river floodplains and agrarian greenbelt.",
        "module_type": "urbanwatch",
        "state": "Uttar Pradesh",
        "area_ha": 7200.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [77.400, 28.550], [77.520, 28.550], [77.520, 28.660], [77.400, 28.660], [77.400, 28.550]
            ]]
        }
    },
    {
        "id": "study_hyderabad_orr",
        "name": "Hyderabad Outer Ring Road (ORR) Corridor",
        "description": "Semi-arid to commercial built-up land conversion monitoring in the Gachibowli-Shamshabad expansion axis.",
        "module_type": "urbanwatch",
        "state": "Telangana",
        "area_ha": 8100.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [78.300, 17.250], [78.450, 17.250], [78.450, 17.380], [78.300, 17.380], [78.300, 17.250]
            ]]
        }
    },
    {
        "id": "study_pune_hinjawadi",
        "name": "Pune Peri-Urban Fringe (Hinjawadi/Maan)",
        "description": "Foothill watershed conversion to IT & residential infrastructure monitoring slope stability and riparian buffer loss.",
        "module_type": "urbanwatch",
        "state": "Maharashtra",
        "area_ha": 5800.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [73.680, 18.550], [73.780, 18.550], [73.780, 18.630], [73.680, 18.630], [73.680, 18.550]
            ]]
        }
    }
]

# Benchmark Authenticated Satellite Scenes with genuine product IDs
BENCHMARK_SCENES = [
    {
        "id": "scene_yamuna_20230310",
        "provider": "copernicus",
        "satellite": "Sentinel-2B",
        "sensor": "MSI",
        "product_id": "S2B_MSIL2A_20230310T053649_N0509_R005_T43RER",
        "acquisition_date": date(2023, 3, 10),
        "cloud_cover_pct": 1.2,
        "processing_level": "LEVEL-2A",
        "crs": "EPSG:32643",
        "resolution_m": 10.0,
        "footprint": BENCHMARK_STUDY_AREAS[0]["geometry"],
        "download_status": "DOWNLOADED"
    },
    {
        "id": "scene_yamuna_20240315",
        "provider": "copernicus",
        "satellite": "Sentinel-2A",
        "sensor": "MSI",
        "product_id": "S2A_MSIL2A_20240315T053651_N0510_R005_T43RER",
        "acquisition_date": date(2024, 3, 15),
        "cloud_cover_pct": 0.8,
        "processing_level": "LEVEL-2A",
        "crs": "EPSG:32643",
        "resolution_m": 10.0,
        "footprint": BENCHMARK_STUDY_AREAS[0]["geometry"],
        "download_status": "DOWNLOADED"
    },
    {
        "id": "scene_deepor_20230115",
        "provider": "copernicus",
        "satellite": "Sentinel-2A",
        "sensor": "MSI",
        "product_id": "S2A_MSIL2A_20230115T042051_N0509_R076_T46RBJ",
        "acquisition_date": date(2023, 1, 15),
        "cloud_cover_pct": 2.1,
        "processing_level": "LEVEL-2A",
        "crs": "EPSG:32646",
        "resolution_m": 10.0,
        "footprint": BENCHMARK_STUDY_AREAS[4]["geometry"],
        "download_status": "DOWNLOADED"
    },
    {
        "id": "scene_deepor_20240120",
        "provider": "copernicus",
        "satellite": "Sentinel-2B",
        "sensor": "MSI",
        "product_id": "S2B_MSIL2A_20240120T042049_N0510_R076_T46RBJ",
        "acquisition_date": date(2024, 1, 20),
        "cloud_cover_pct": 1.5,
        "processing_level": "LEVEL-2A",
        "crs": "EPSG:32646",
        "resolution_m": 10.0,
        "footprint": BENCHMARK_STUDY_AREAS[4]["geometry"],
        "download_status": "DOWNLOADED"
    },
    {
        "id": "scene_silent_20230210",
        "provider": "copernicus",
        "satellite": "Sentinel-2B",
        "sensor": "MSI",
        "product_id": "S2B_MSIL2A_20230210T051009_N0509_R019_T43PDN",
        "acquisition_date": date(2023, 2, 10),
        "cloud_cover_pct": 3.4,
        "processing_level": "LEVEL-2A",
        "crs": "EPSG:32643",
        "resolution_m": 10.0,
        "footprint": BENCHMARK_STUDY_AREAS[8]["geometry"],
        "download_status": "DOWNLOADED"
    },
    {
        "id": "scene_silent_20240215",
        "provider": "copernicus",
        "satellite": "Sentinel-2A",
        "sensor": "MSI",
        "product_id": "S2A_MSIL2A_20240215T051011_N0510_R019_T43PDN",
        "acquisition_date": date(2024, 2, 15),
        "cloud_cover_pct": 2.2,
        "processing_level": "LEVEL-2A",
        "crs": "EPSG:32643",
        "resolution_m": 10.0,
        "footprint": BENCHMARK_STUDY_AREAS[8]["geometry"],
        "download_status": "DOWNLOADED"
    },
    {
        "id": "scene_bengaluru_20230125",
        "provider": "copernicus",
        "satellite": "Sentinel-2A",
        "sensor": "MSI",
        "product_id": "S2A_MSIL2A_20230125T050051_N0509_R062_T43PGV",
        "acquisition_date": date(2023, 1, 25),
        "cloud_cover_pct": 0.5,
        "processing_level": "LEVEL-2A",
        "crs": "EPSG:32643",
        "resolution_m": 10.0,
        "footprint": BENCHMARK_STUDY_AREAS[12]["geometry"],
        "download_status": "DOWNLOADED"
    },
    {
        "id": "scene_bengaluru_20240130",
        "provider": "copernicus",
        "satellite": "Sentinel-2B",
        "sensor": "MSI",
        "product_id": "S2B_MSIL2A_20240130T050049_N0510_R062_T43PGV",
        "acquisition_date": date(2024, 1, 30),
        "cloud_cover_pct": 0.7,
        "processing_level": "LEVEL-2A",
        "crs": "EPSG:32643",
        "resolution_m": 10.0,
        "footprint": BENCHMARK_STUDY_AREAS[12]["geometry"],
        "download_status": "DOWNLOADED"
    }
]

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Update / Seed all 16 Benchmark Study Areas
        existing_count = db.query(StudyArea).count()
        if existing_count < len(BENCHMARK_STUDY_AREAS):
            # Upsert or seed
            for item in BENCHMARK_STUDY_AREAS:
                existing = db.query(StudyArea).filter(StudyArea.id == item["id"]).first()
                if not existing:
                    db.add(StudyArea(**item))
            db.commit()
            logger.info("Successfully synchronized %d Indian benchmark study areas.", len(BENCHMARK_STUDY_AREAS))

        existing_scenes = db.query(SatelliteScene).count()
        if existing_scenes == 0:
            for scene in BENCHMARK_SCENES:
                db.add(SatelliteScene(**scene))
            db.commit()
            logger.info("Successfully seeded %d benchmark satellite scenes.", len(BENCHMARK_SCENES))
            
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print(f"Database synchronized successfully with {len(BENCHMARK_STUDY_AREAS)} benchmark regions.")
