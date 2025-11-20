@echo off
REM Twiddler Driver Startup Script for Windows
REM This script starts the Twiddler driver with proper configuration

echo Starting Twiddler Driver...
echo.

REM Change to the Twiddler installation directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import serial, keyboard, mouse" >nul 2>&1
if errorlevel 1 (
    echo Error: Required Python packages not installed
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Start the driver
echo.
echo Starting Twiddler driver...
echo Press Ctrl+C to stop
echo.
python src\twiddler_driver.py

pause
