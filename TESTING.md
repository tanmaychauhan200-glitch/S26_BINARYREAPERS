# TESTING STRATEGY & TEST SUITE

---

## 1. Test Architecture
Tests are divided into two clear layers:
1. **Mathematical & Algorithmic Unit Tests**: Use controlled synthetic numpy rasters with known spatial configurations to assert numerical and index correctness without external network dependencies.
2. **API Endpoint & Contract Tests**: Use FastAPI `TestClient` to verify HTTP status codes, JSON response schemas, and error handling.

---

## 2. Running Tests
From the `backend/` directory:
```powershell
pytest -v
```

---

## 3. Test Coverage Matrix
- `test_indices.py`: Asserts NDWI, MNDWI, NDVI, NDBI values on positive, negative, and zero denominator bounds.
- `test_riverwatch.py`: Verifies channel boundary extraction and transect width difference.
- `test_wetlandwatch.py`: Asserts seasonal persistence classification.
- `test_forestguard.py`: Asserts dNDVI disturbance thresholding and patch metric calculations.
- `test_urbanwatch.py`: Asserts impervious surface identification and buffer proximity calculations.
- `test_api.py`: Validates `/health`, `/study-areas`, `/jobs/run`, and `/results`.
