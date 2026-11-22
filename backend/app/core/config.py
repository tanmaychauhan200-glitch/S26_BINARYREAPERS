import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "TerraWatch 360"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    # Server configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    
    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'terrawatch.db'}"
    
    # Storage Paths
    DATA_RAW_DIR: Path = BASE_DIR / "data" / "raw"
    DATA_INTERMEDIATE_DIR: Path = BASE_DIR / "data" / "intermediate"
    DATA_PROCESSED_DIR: Path = BASE_DIR / "data" / "processed"
    DATA_TEST_DIR: Path = BASE_DIR / "data" / "test"
    OUTPUTS_MAPS_DIR: Path = BASE_DIR / "outputs" / "maps"
    OUTPUTS_REPORTS_DIR: Path = BASE_DIR / "outputs" / "reports"
    
    # Satellite Providers
    COPERNICUS_STAC_URL: str = "https://stac.dataspace.copernicus.eu/v1"
    COPERNICUS_TOKEN_URL: str = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    COPERNICUS_CLIENT_ID: str = ""
    COPERNICUS_CLIENT_SECRET: str = ""
    
    BHOONIDHI_API_URL: str = "https://bhoonidhi.nrsc.gov.in/bhoonidhi-api"
    BHOONIDHI_API_KEY: str = ""
    
    OFFLINE_DEMO_MODE: bool = True
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# Ensure required runtime directories exist
for path in [
    settings.DATA_RAW_DIR,
    settings.DATA_INTERMEDIATE_DIR,
    settings.DATA_PROCESSED_DIR,
    settings.DATA_TEST_DIR,
    settings.OUTPUTS_MAPS_DIR,
    settings.OUTPUTS_REPORTS_DIR
]:
    path.mkdir(parents=True, exist_ok=True)
