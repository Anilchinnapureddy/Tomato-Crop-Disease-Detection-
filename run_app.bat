@echo off
title AgroSense AI - Tomato Crop Health & Irrigation Suite
echo ============================================================
echo   AGROSENSE AI: TOMATO CROP DISEASE & SMART IRRIGATION
echo ============================================================
echo.
echo Select Web Application Interface to launch:
echo   [1] Streamlit UI (Recommended - Multi-Page, AI Chat & Water Advisor)
echo   [2] Flask UI (Traditional Web Dashboard)
echo.
set /p choice="Enter choice [1 or 2] (Default is 1): "

cd /d "%~dp0"
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found. Using system Python...
)

if "%choice%"=="2" (
    echo Starting Flask Web Application at http://127.0.0.1:5000 ...
    python app.py
) else (
    echo Starting Streamlit Multi-Page Web Application at http://localhost:8501 ...
    streamlit run streamlit_app.py --server.port 8501 --browser.gatherUsageStats false
)

pause
