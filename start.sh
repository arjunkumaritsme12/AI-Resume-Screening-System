#!/bin/bash

# AI Resume Screening System - Quick Start Script for macOS/Linux

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   AI Resume Screening System - Setup & Launch        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "✓ Python detected"
python3 --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "✗ Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

# Run tests
echo "Running system tests..."
python test_system.py
if [ $? -ne 0 ]; then
    echo "✗ System tests failed"
    echo "Check the errors above and try again"
    exit 1
fi
echo ""

# Launch Streamlit
echo ""
echo "════════════════════════════════════════════════════════"
echo "✓ Setup complete! Starting application..."
echo "════════════════════════════════════════════════════════"
echo ""
echo "The application will open in your browser at:"
echo "  http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

cd app
streamlit run app.py
