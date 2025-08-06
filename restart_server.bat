@echo off
echo ========================================
echo TFT QA Bot - Server Restart Script
echo ========================================
echo.

echo [1/5] Stopping all Python processes...
taskkill /F /IM python.exe 2>nul
if %errorlevel% equ 0 (
    echo ✓ Python processes stopped
) else (
    echo - No Python processes were running
)
echo.

echo [2/5] Removing Python cache files...
if exist __pycache__ (
    rmdir /s /q __pycache__
    echo ✓ Python cache cleared
) else (
    echo - No Python cache found
)
echo.

echo [3/5] Removing Next.js cache...
if exist .next (
    rmdir /s /q .next
    echo ✓ Next.js cache cleared
) else (
    echo - No Next.js cache found
)
echo.

echo [4/5] Starting backend server...
start "TFT QA Bot Backend" cmd /k "python backend_server.py"
echo ✓ Backend server started
echo.

echo [5/5] Starting frontend server...
start "TFT QA Bot Frontend" cmd /k "npm run dev"
echo ✓ Frontend server started
echo.

echo ========================================
echo ✓ Server restart complete!
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Please wait 10-15 seconds for servers to fully start.
echo Then open http://localhost:3000 in your browser.
echo.
pause 