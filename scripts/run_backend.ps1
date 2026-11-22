Write-Host "Starting TerraWatch 360 FastAPI Backend..." -ForegroundColor Cyan
& "C:\Users\ASUS\anaconda3\python.exe" -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
