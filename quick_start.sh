#!/bin/bash
# Quick Start - Interactive Testing

cd "$(dirname "$0")/backend"

echo "🎮 Calendar ERP Chatbot - Quick Start"
echo ""
echo "Choose testing mode:"
echo ""
echo "  1. Interactive (Colorful) - Recommended ⭐"
echo "  2. Interactive (Simple)"
echo "  3. Quick Test (Automated)"
echo "  4. API Server Mode"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Starting colorful interactive mode..."
        python test_interactive.py
        ;;
    2)
        echo ""
        echo "Starting simple interactive mode..."
        python test_simple.py
        ;;
    3)
        echo ""
        echo "Running quick automated test..."
        python test_quick.py
        ;;
    4)
        echo ""
        echo "Starting API server..."
        echo "After it starts, open another terminal and run: python test_api.py"
        ./start.sh
        ;;
    *)
        echo ""
        echo "Invalid choice. Running colorful mode by default..."
        python test_interactive.py
        ;;
esac
