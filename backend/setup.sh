#!/bin/bash

# Setup script for Calendar ERP Chatbot
# This script helps you get started quickly

set -e

echo "🚀 Calendar ERP Chatbot - Setup Script"
echo "======================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1,2)
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "📦 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your GOOGLE_API_KEY"
    echo "   You can get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
    read -p "Press Enter to continue after you've added your API key..."
else
    echo "✅ .env file already exists"
fi

# Check if API key is set
source .env
if [ -z "$GOOGLE_API_KEY" ] || [ "$GOOGLE_API_KEY" = "your_google_api_key_here" ]; then
    echo "❌ GOOGLE_API_KEY is not set in .env file"
    echo "   Please edit .env and add your API key, then run this script again."
    exit 1
fi

# Create data directory
mkdir -p data/vectorstore

# Initialize vector store
echo "🔍 Initializing vector store with calendar data..."
python scripts/initialize_db.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Or simply run:"
echo "  ./run.sh"
echo ""
echo "The API will be available at:"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo ""
