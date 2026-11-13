@echo off
title AgroSense AI - Tomato Crop Health and Irrigation Dashboard (Streamlit)
echo ============================================================
echo Starting AgroSense AI Streamlit Multi-Page Web Application...
echo ============================================================
cd /d "%~dp0"
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found. Using system Python...
)

echo Opening Streamlit application at http://localhost:8501 ...
streamlit run streamlit_app.py --server.port 8501 --browser.gatherUsageStats false
pause
