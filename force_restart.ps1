# Force Restart Script - Complete Reset
Write-Host "========================================" -ForegroundColor Red
Write-Host "TFT QA Bot - FORCE RESTART" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

# Step 1: Kill ALL related processes
Write-Host "[1/6] Killing ALL related processes..." -ForegroundColor Yellow
$processes = @("python", "node", "npm")
foreach ($proc in $processes) {
    Get-Process -Name $proc -ErrorAction SilentlyContinue | Stop-Process -Force
    Write-Host "Killed $proc processes" -ForegroundColor Green
}
Write-Host ""

# Step 2: Remove ALL cache directories
Write-Host "[2/6] Removing ALL cache directories..." -ForegroundColor Yellow
$cacheDirs = @("__pycache__", ".next", "node_modules")
foreach ($dir in $cacheDirs) {
    if (Test-Path $dir) {
        Remove-Item -Recurse -Force $dir
        Write-Host "Removed $dir" -ForegroundColor Green
    } else {
        Write-Host "$dir not found" -ForegroundColor Gray
    }
}
Write-Host ""

# Step 3: Remove ALL Python cache files
Write-Host "[3/6] Removing ALL Python cache files..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Name "*.pyc" -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item $_ -Force
    Write-Host "Removed $_" -ForegroundColor Green
}
Write-Host ""

# Step 4: Reinstall node_modules
Write-Host "[4/6] Reinstalling node_modules..." -ForegroundColor Yellow
npm install
Write-Host "Node modules reinstalled" -ForegroundColor Green
Write-Host ""

# Step 5: Start backend with fresh environment
Write-Host "[5/6] Starting backend server..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "backend_server.py" -WindowStyle Normal
Write-Host "Backend started" -ForegroundColor Green
Write-Host ""

# Step 6: Start frontend
Write-Host "[6/6] Starting frontend server..." -ForegroundColor Yellow
Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WindowStyle Normal
Write-Host "Frontend started" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "FORCE RESTART COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend: http://localhost:5000" -ForegroundColor White
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "WAIT 30 SECONDS for servers to fully start!" -ForegroundColor Red
Write-Host "Then open http://localhost:3000 and test with Ctrl+Shift+R" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter when ready to test" 