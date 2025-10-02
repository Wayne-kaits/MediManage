@echo off
title Hospital Management System

echo.
echo ================================================================
echo  Hospital Management System - Desktop Application
echo  Publisher: Kaitsnet IT Solutions
echo ================================================================
echo.

REM Check if we're in the correct directory
if not exist "desktop_app.py" (
    echo ERROR: desktop_app.py not found!
    echo.
    echo Please run this script from the WindowsDesktopApp directory.
    echo Current directory: %CD%
    echo.
    echo To fix this:
    echo 1. Navigate to the WindowsDesktopApp folder
    echo 2. Run this script again
    echo.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Or run setup.bat to install dependencies
    echo.
    pause
    exit /b 1
)

echo Starting Hospital Management System...
echo.

REM Run the application
python launch.py

echo.
echo Application closed.
pause 