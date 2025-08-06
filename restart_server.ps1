# TFT QA Bot - Server Restart Script (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TFT QA Bot - Server Restart Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Stop all Python processes
Write-Host "[1/5] Stopping all Python processes..." -ForegroundColor Yellow
$pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Stop-Process -Name "python" -Force
    Write-Host "✓ Python processes stopped" -ForegroundColor Green
} else {
    Write-Host "- No Python processes were running" -ForegroundColor Gray
}
Write-Host ""

# Step 2: Remove Python cache
Write-Host "[2/5] Removing Python cache files..." -ForegroundColor Yellow
if (Test-Path "__pycache__") {
    Remove-Item -Recurse -Force "__pycache__"
    Write-Host "✓ Python cache cleared" -ForegroundColor Green
} else {
    Write-Host "- No Python cache found" -ForegroundColor Gray
}
Write-Host ""

# Step 3: Remove Next.js cache
Write-Host "[3/5] Removing Next.js cache..." -ForegroundColor Yellow
if (Test-Path ".next") {
    Remove-Item -Recurse -Force ".next"
    Write-Host "✓ Next.js cache cleared" -ForegroundColor Green
} else {
    Write-Host "- No Next.js cache found" -ForegroundColor Gray
}
Write-Host ""

# Step 4: Start backend server
Write-Host "[4/5] Starting backend server..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "backend_server.py" -WindowStyle Normal
Write-Host "✓ Backend server started" -ForegroundColor Green
Write-Host ""

# Step 5: Start frontend server
Write-Host "[5/5] Starting frontend server..." -ForegroundColor Yellow
Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WindowStyle Normal
Write-Host "✓ Frontend server started" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Server restart complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend: http://localhost:5000" -ForegroundColor White
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Please wait 10-15 seconds for servers to fully start." -ForegroundColor Yellow
Write-Host "Then open http://localhost:3000 in your browser." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue" 