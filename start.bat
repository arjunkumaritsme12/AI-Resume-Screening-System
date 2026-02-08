@echo off
REM AI Resume Screening System - Quick Start Script for Windows

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   AI Resume Screening System - Setup & Launch        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python detected
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo ✓ Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install/upgrade requirements
echo Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Run tests
echo Running system tests...
python test_system.py
if errorlevel 1 (
    echo ✗ System tests failed
    echo Check the errors above and try again
    pause
    exit /b 1
)
echo.

REM Launch Streamlit
echo.
echo ════════════════════════════════════════════════════════
echo ✓ Setup complete! Starting application...
echo ════════════════════════════════════════════════════════
echo.
echo The application will open in your browser at:
echo   http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

cd app
streamlit run app.py

pause
