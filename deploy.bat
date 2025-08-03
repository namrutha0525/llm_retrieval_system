@echo off
echo 🚀 Starting LLM Retrieval System v2 Deployment...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.10+ first.
    pause
    exit /b 1
)

echo 📦 Creating virtual environment...
python -m venv venv

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

echo 📥 Installing dependencies...
pip install -r requirements.txt

echo ✅ Checking dependencies...
python -c "import fastapi, uvicorn, aiohttp, requests; print('All dependencies installed successfully!')"

echo 🔧 Setting up environment...
set GEMINI_API_KEY=AIzaSyCyLEILSjE96HexvyxwFw_S-aEvz8GQ3N

echo.
echo 🎯 Starting FastAPI server...
echo ======================================
echo Server URL: http://localhost:8000
echo Health Check: http://localhost:8000/health
echo API Endpoint: http://localhost:8000/api/v1/hackrx/run
echo API Docs: http://localhost:8000/docs
echo.
echo Bearer Token: 479309883e76b7aff59e87e1e032ce655934c42516b75cc1ceaea8663351e3ba
echo.
echo To stop the server, press Ctrl+C
echo ======================================
echo.

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
