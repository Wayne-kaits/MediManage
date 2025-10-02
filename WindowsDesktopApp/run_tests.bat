@echo off
title Hospital Management System - Test Suite

echo.
echo ================================================================
echo  Hospital Management System - Test Suite
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
    pause
    exit /b 1
)

echo Running test suite...
echo.

python test_build.py

echo.
echo Test suite completed.
echo Check test_report.txt for detailed results.
echo.

pause 