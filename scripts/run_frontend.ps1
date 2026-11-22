Write-Host "Starting TerraWatch 360 React Frontend..." -ForegroundColor Cyan
$env:PATH = "C:\Users\ASUS\AppData\Local\nodejs;" + $env:PATH
Set-Location frontend
& "C:\Users\ASUS\AppData\Local\nodejs\npm.cmd" run dev
