#!/bin/bash

# Simple startup script for Calendar ERP Chatbot
# This script starts the FastAPI server without requiring a virtual environment

set -e

echo "🚀 Starting Calendar ERP Chatbot..."
echo ""

# Change to backend directory
cd "$(dirname "$0")"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "   Please ensure .env file exists with GOOGLE_API_KEY"
    exit 1
fi

# Load environment variables from .env
export $(grep -v '^#' .env | xargs)

# Set PYTHONPATH
export PYTHONPATH="$(pwd)"

echo "✅ Environment configured"
echo "📦 API Model: ${LLM_MODEL:-gemini-2.5-flash}"
echo "🗄️  Vector Store: ${VECTOR_DB_PATH}"
echo ""
echo "Starting server on ${API_HOST:-0.0.0.0}:${API_PORT:-8000}..."
echo "API Documentation: http://localhost:${API_PORT:-8000}/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python -m uvicorn app.main:app --reload --host "${API_HOST:-0.0.0.0}" --port "${API_PORT:-8000}"
