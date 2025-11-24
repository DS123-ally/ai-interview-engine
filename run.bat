@echo off
REM AI Interview Engine - Windows Local Setup & Run Script

echo 🤖 AI Interview Engine - Local Setup
echo ==================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies...
cd workshop\ai-interview-clean
pip install -r requirements_bedrock.txt

REM Run the application
echo 🚀 Starting AI Interview Engine...
echo 📱 Open: http://localhost:8501
echo ⏹️  Press Ctrl+C to stop

python -m streamlit run advanced_analytics_app.py --server.port 8501 --server.address 0.0.0.0