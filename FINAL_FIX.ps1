Write-Host "TFT QA Bot - FINAL COMPLETE FIX" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

# Step 1: Kill ALL processes
Write-Host "[1/6] Killing ALL processes..." -ForegroundColor Yellow
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process -Name "node" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "All processes stopped" -ForegroundColor Green

# Step 2: Remove ALL caches
Write-Host "[2/6] Removing ALL caches..." -ForegroundColor Yellow
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__" }
if (Test-Path ".next") { Remove-Item -Recurse -Force ".next" }
if (Test-Path "node_modules") { Remove-Item -Recurse -Force "node_modules" }
Write-Host "All caches removed" -ForegroundColor Green

# Step 3: Reinstall dependencies
Write-Host "[3/6] Reinstalling dependencies..." -ForegroundColor Yellow
npm install
Write-Host "Dependencies reinstalled" -ForegroundColor Green

# Step 4: Start backend
Write-Host "[4/6] Starting backend server..." -ForegroundColor Yellow
Start-Process -FilePath "cmd" -ArgumentList "/k", "python backend_server.py" -WindowStyle Normal
Write-Host "Backend started" -ForegroundColor Green

# Step 5: Wait for backend to initialize
Write-Host "[5/6] Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Step 6: Start frontend
Write-Host "[6/6] Starting frontend server..." -ForegroundColor Yellow
Start-Process -FilePath "cmd" -ArgumentList "/k", "npm run dev" -WindowStyle Normal
Write-Host "Frontend started" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "FINAL FIX COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend: http://localhost:5000" -ForegroundColor White
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "WAIT 30 SECONDS for servers to fully start!" -ForegroundColor Red
Write-Host ""
Write-Host "CRITICAL STEPS:" -ForegroundColor Yellow
Write-Host "1. Open http://localhost:3000" -ForegroundColor White
Write-Host "2. Press Ctrl+Shift+R (hard refresh)" -ForegroundColor White
Write-Host "3. Click 'Clear Chat' button if available" -ForegroundColor White
Write-Host "4. Test with: 'List all 2-cost champions'" -ForegroundColor White
Write-Host ""
Write-Host "This should now work for ALL cost tiers!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter when ready to test" 