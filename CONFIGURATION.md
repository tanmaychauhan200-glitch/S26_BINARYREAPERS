# CONFIGURATION GUIDE — TERRAWATCH 360

Create a `.env` file in the root or `backend/` directory based on `.env.example`.

```env
# Server
HOST=127.0.0.1
PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173"]

# Database
DATABASE_URL=sqlite:///./terrawatch.db

# Storage Directories
DATA_RAW_DIR=./data/raw
DATA_PROCESSED_DIR=./data/processed
OUTPUTS_DIR=./outputs

# Copernicus Data Space Ecosystem (CDSE)
COPERNICUS_CLIENT_ID=
COPERNICUS_CLIENT_SECRET=
COPERNICUS_STAC_URL=https://stac.dataspace.copernicus.eu/v1

# ISRO Bhoonidhi
BHOONIDHI_API_KEY=
BHOONIDHI_API_URL=https://bhoonidhi.nrsc.gov.in/bhoonidhi-api

# Offline Demo Mode
OFFLINE_DEMO_MODE=true
```
