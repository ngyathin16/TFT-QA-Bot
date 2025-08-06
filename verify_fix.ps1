Write-Host "TFT QA Bot - Verify Fix" -ForegroundColor Cyan
Write-Host ""

# Test backend directly
Write-Host "[1/3] Testing backend API..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/chat" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"message": "List all 2-cost champions"}' -TimeoutSec 10
    $data = $response.Content | ConvertFrom-Json
    $hasChampions = $data.response -match "Janna|Jhin|Kai|Katarina|Kobuko|Lux|Rakan|Xayah|Xin Zhao|Gangplank|Dr\. Mundo|Vi|Shen"
    
    if ($hasChampions) {
        Write-Host "✅ Backend API: WORKING (returns actual champion names)" -ForegroundColor Green
    } else {
        Write-Host "❌ Backend API: NOT WORKING (returns generic responses)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Backend API: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

# Test Next.js API
Write-Host "[2/3] Testing Next.js API..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/api/chat" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"message": "List all 2-cost champions"}' -TimeoutSec 10
    $data = $response.Content | ConvertFrom-Json
    $hasChampions = $data.response -match "Janna|Jhin|Kai|Katarina|Kobuko|Lux|Rakan|Xayah|Xin Zhao|Gangplank|Dr\. Mundo|Vi|Shen"
    
    if ($hasChampions) {
        Write-Host "✅ Next.js API: WORKING (returns actual champion names)" -ForegroundColor Green
    } else {
        Write-Host "❌ Next.js API: NOT WORKING (returns generic responses)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Next.js API: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

# Check if servers are running
Write-Host "[3/3] Checking server status..." -ForegroundColor Yellow
$pythonRunning = Get-Process -Name "python" -ErrorAction SilentlyContinue
$nodeRunning = Get-Process -Name "node" -ErrorAction SilentlyContinue

if ($pythonRunning) {
    Write-Host "✅ Python server: RUNNING" -ForegroundColor Green
} else {
    Write-Host "❌ Python server: NOT RUNNING" -ForegroundColor Red
}

if ($nodeRunning) {
    Write-Host "✅ Node.js server: RUNNING" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js server: NOT RUNNING" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verification Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "If you see any ❌ errors, run: .\FINAL_FIX.ps1" -ForegroundColor Yellow
Write-Host "If everything shows ✅, your chatbot is working correctly!" -ForegroundColor Green 