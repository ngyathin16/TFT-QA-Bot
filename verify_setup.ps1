# Verification Script - Check if everything is working
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TFT QA Bot - Setup Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if servers are running
Write-Host "[1/4] Checking if servers are running..." -ForegroundColor Yellow
$pythonRunning = Get-Process -Name "python" -ErrorAction SilentlyContinue
$nodeRunning = Get-Process -Name "node" -ErrorAction SilentlyContinue

if ($pythonRunning) {
    Write-Host "✅ Python server is running" -ForegroundColor Green
} else {
    Write-Host "❌ Python server is NOT running" -ForegroundColor Red
}

if ($nodeRunning) {
    Write-Host "✅ Node.js server is running" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js server is NOT running" -ForegroundColor Red
}
Write-Host ""

# Test backend health
Write-Host "[2/4] Testing backend health..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -Method GET -TimeoutSec 5
    if ($healthResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend is responding" -ForegroundColor Green
    } else {
        Write-Host "❌ Backend returned status: $($healthResponse.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Backend is not responding: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test enhanced search
Write-Host "[3/4] Testing enhanced search..." -ForegroundColor Yellow
try {
    $searchResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/test-enhanced-search" -Method GET -TimeoutSec 5
    if ($searchResponse.StatusCode -eq 200) {
        $data = $searchResponse.Content | ConvertFrom-Json
        if ($data.status -eq "working") {
            Write-Host "✅ Enhanced search is working" -ForegroundColor Green
        } else {
            Write-Host "❌ Enhanced search is NOT working" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Enhanced search test failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Enhanced search test failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test actual champion listing
Write-Host "[4/4] Testing champion listing..." -ForegroundColor Yellow
try {
    $chatResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/chat" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"message": "List all 2-cost champions"}' -TimeoutSec 10
    if ($chatResponse.StatusCode -eq 200) {
        $data = $chatResponse.Content | ConvertFrom-Json
        $response = $data.response
        
        # Check if response contains actual champion names
        $hasChampions = $response -match "Janna|Jhin|Kai|Katarina|Kobuko|Lux|Rakan|Xayah|Xin Zhao|Gangplank|Dr\. Mundo|Vi|Shen"
        
        if ($hasChampions) {
            Write-Host "✅ Champion listing is working correctly" -ForegroundColor Green
            Write-Host "Sample response: $($response.Substring(0, [Math]::Min(100, $response.Length)))..." -ForegroundColor Gray
        } else {
            Write-Host "❌ Champion listing is NOT working correctly" -ForegroundColor Red
            Write-Host "Response: $($response.Substring(0, [Math]::Min(200, $response.Length)))..." -ForegroundColor Gray
        }
    } else {
        Write-Host "❌ Chat API test failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Chat API test failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verification Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "If you see any ❌ errors above, run:" -ForegroundColor Yellow
Write-Host "  .\force_restart.ps1" -ForegroundColor White
Write-Host ""
Write-Host "If everything shows ✅, your chatbot is working correctly!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to continue" 