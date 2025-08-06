# Simple TFT QA Bot Restart Script
Write-Host "TFT QA Bot - Simple Restart Script" -ForegroundColor Cyan
Write-Host ""

# Stop Python processes
Write-Host "Stopping Python processes..." -ForegroundColor Yellow
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "Python processes stopped" -ForegroundColor Green

# Remove caches
Write-Host "Removing caches..." -ForegroundColor Yellow
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__" }
if (Test-Path ".next") { Remove-Item -Recurse -Force ".next" }
Write-Host "Caches cleared" -ForegroundColor Green

# Start servers
Write-Host "Starting servers..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "backend_server.py" -WindowStyle Normal
Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WindowStyle Normal

Write-Host "Servers started!" -ForegroundColor Green
Write-Host "Backend: http://localhost:5000" -ForegroundColor White
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "Wait 10-15 seconds, then open http://localhost:3000" -ForegroundColor Yellow 