@echo off
REM Data Masking Tool - Setup Script for Windows
REM This script sets up the environment and installs dependencies

echo ========================================
echo Data Masking Tool - Setup
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Setup Complete!
    echo ========================================
    echo.
    echo To run the application:
    echo   python data_masking_tool.py
    echo.
    echo To run the demo:
    echo   python test_demo.py
    echo.
    echo For help, see README.md or QUICK_START.md
    echo.
) else (
    echo ERROR: Failed to install dependencies
    echo Try running manually: pip install pandas openpyxl Faker cryptography
    pause
    exit /b 1
)

pause
