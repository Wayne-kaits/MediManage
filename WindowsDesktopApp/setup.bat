@echo off
title Hospital Management System - Setup

echo.
echo ================================================================
echo  Hospital Management System - Setup
echo  Publisher: Kaitsnet IT Solutions
echo  Version: 1.0.0
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
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python detected. Installing dependencies...
echo.

REM Install required packages
echo Installing required packages...

python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip
    pause
    exit /b 1
)

echo Installing tkcalendar...
python -m pip install tkcalendar==1.6.1
if errorlevel 1 (
    echo Failed to install tkcalendar
    pause
    exit /b 1
)

echo Installing matplotlib...
python -m pip install matplotlib==3.7.2
if errorlevel 1 (
    echo Failed to install matplotlib
    pause
    exit /b 1
)

echo Installing pandas...
python -m pip install pandas==2.0.3
if errorlevel 1 (
    echo Failed to install pandas
    pause
    exit /b 1
)

echo Installing Pillow...
python -m pip install Pillow==10.0.0
if errorlevel 1 (
    echo Failed to install Pillow
    pause
    exit /b 1
)

echo Installing PyInstaller (for building installer)...
python -m pip install pyinstaller
if errorlevel 1 (
    echo Warning: Failed to install PyInstaller
    echo You can still run the application, but cannot build the installer
)

echo.
echo ================================================================
echo  Setup completed successfully!
echo ================================================================
echo.
echo You can now:
echo   1. Run the application: python launch.py
echo   2. Build installer: python build_installer.py
echo   3. Run tests: python test_build.py
echo.
echo Default login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Remember to change the default password after first login!
echo.

set /p choice="Would you like to start the application now? (y/n): "
if /i "%choice%"=="y" (
    python launch.py
)

pause