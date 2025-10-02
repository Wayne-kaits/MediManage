@echo off
title Hospital Management System

echo.
echo ================================================================
echo  Hospital Management System - Desktop Application
echo  Publisher: Kaitsnet IT Solutions
echo ================================================================
echo.

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

python launch.py

echo.
echo Application closed.
pause 