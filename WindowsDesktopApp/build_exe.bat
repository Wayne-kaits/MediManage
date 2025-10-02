@echo off
title Hospital Management System - EXE Installer Builder

echo.
echo ================================================================
echo  Hospital Management System - Professional EXE Installer Builder
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

echo Python detected. Checking build dependencies...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo PyInstaller installed successfully.
    echo.
)

REM Check if Pillow is installed (for icon creation)
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Pillow not found. Installing...
    python -m pip install Pillow
    if errorlevel 1 (
        echo Failed to install Pillow
        pause
        exit /b 1
    )
    echo Pillow installed successfully.
    echo.
)

echo All dependencies satisfied. Starting build process...
echo.

REM Run the installer builder
python build_installer.py

if errorlevel 1 (
    echo.
    echo Build process encountered an error.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo  Build process completed!
echo  Check the 'dist' folder for the installer executable.
echo ================================================================
echo.

REM Check if installer was created
if exist "dist\HospitalManagementSystem_v1.0.0_Setup.exe" (
    echo ✓ Installer created successfully:
    echo   dist\HospitalManagementSystem_v1.0.0_Setup.exe
    echo.
    echo The installer is ready for distribution!
    echo.
    set /p choice="Would you like to open the dist folder? (y/n): "
    if /i "%choice%"=="y" (
        explorer dist
    )
) else (
    echo ✗ Installer file not found. Build may have failed.
    echo Check the output above for error messages.
)

echo.
pause