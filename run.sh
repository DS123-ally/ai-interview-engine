#!/bin/bash

# AI Interview Engine - Local Setup & Run Script

echo "🤖 AI Interview Engine - Local Setup"
echo "=================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
cd workshop/ai-interview-clean
pip3 install -r requirements_bedrock.txt

# Run the application
echo "🚀 Starting AI Interview Engine..."
echo "📱 Open: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop"

python3 -m streamlit run advanced_analytics_app.py --server.port 8501 --server.address 0.0.0.0