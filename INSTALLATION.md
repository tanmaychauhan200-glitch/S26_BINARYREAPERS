# INSTALLATION & SETUP GUIDE (WINDOWS)

## 1. Prerequisites
- Windows 10/11 (64-bit)
- Anaconda / Miniconda (installed at `C:\Users\ASUS\anaconda3`)
- Node.js (v18+)

---

## 2. Python Environment Setup
Open PowerShell or Anaconda Prompt:

```powershell
# Create dedicated Python 3.12 environment with conda-forge
conda create -n terrawatch python=3.12 -c conda-forge -y
conda activate terrawatch

# Install core geospatial dependencies from conda-forge
conda install -c conda-forge numpy pandas rasterio geopandas shapely pyproj scipy matplotlib -y

# Navigate to backend directory and install FastAPI stack
cd backend
pip install -r requirements.txt
```

---

## 3. Frontend Setup
```powershell
cd ../frontend
npm install
```

---

## 4. Running the Application

### Start Backend API:
```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Start Frontend UI:
```powershell
cd frontend
npm run dev
```

Visit `http://localhost:5173` in your browser.
