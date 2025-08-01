#!/bin/bash

# LLM Retrieval System Deployment Script
echo "🚀 Starting LLM Retrieval System Deployment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if all dependencies are installed
echo "✅ Checking dependencies..."
python3 -c "import fastapi, uvicorn, pdfplumber, sentence_transformers, faiss, aiohttp; print('All dependencies installed successfully!')"

# Set environment variables
echo "🔧 Setting up environment..."
export GEMINI_API_KEY="AIzaSyCyLEILSjE96HexvyxwFw_S-aEvz8GQ3NI"

# Start the server
echo "🎯 Starting FastAPI server..."
echo "Server will be available at: http://localhost:8000"
echo "API endpoint: http://localhost:8000/api/v1/hackrx/run"
echo "Health check: http://localhost:8000/"
echo ""
echo "To stop the server, press Ctrl+C"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
