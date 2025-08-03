#!/bin/bash

# LLM Retrieval System v2 - Local Deployment Script
echo "🚀 Starting LLM Retrieval System v2 Deployment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

echo "📦 Creating virtual environment..."
python3 -m venv venv

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "⬆️ Upgrading pip..."
pip install --upgrade pip

echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Checking dependencies..."
python3 -c "import fastapi, uvicorn, aiohttp, requests; print('All dependencies installed successfully!')"

echo "🔧 Setting up environment..."
export GEMINI_API_KEY="AIzaSyCyLEILSjE96HexvyxwFw_S-aEvz8GQ3N"

echo ""
echo "🎯 Starting FastAPI server..."
echo "======================================"
echo "Server URL: http://localhost:8000"
echo "Health Check: http://localhost:8000/health"
echo "API Endpoint: http://localhost:8000/api/v1/hackrx/run"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Bearer Token: 479309883e76b7aff59e87e1e032ce655934c42516b75cc1ceaea8663351e3ba"
echo ""
echo "To stop the server, press Ctrl+C"
echo "======================================"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
