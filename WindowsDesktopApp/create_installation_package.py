#!/usr/bin/env python3
"""
Hospital Management System - Installation Package Creator
Creates a complete installation package with all necessary files
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_installation_package():
    """Create a complete installation package"""
    print("Hospital Management System - Installation Package Creator")
    print("=" * 60)
    
    # Configuration
    app_name = "Hospital Management System"
    app_version = "1.0.0"
    package_name = f"HospitalManagementSystem_v{app_version}_Complete_Package.zip"
    
    # Directories
    current_dir = Path(__file__).parent
    dist_dir = current_dir / "dist"
    package_dir = dist_dir / "complete_package"
    
    # Create package directory
    package_dir.mkdir(exist_ok=True)
    
    print(f"Creating complete installation package for {app_name} v{app_version}")
    print(f"Output: {dist_dir / package_name}")
    
    # Step 1: Copy main executable
    print("\nStep 1: Copying main executable...")
    installer_exe = dist_dir / "HospitalManagementSystem_v1.0.0_Setup.exe"
    if installer_exe.exists():
        shutil.copy2(installer_exe, package_dir / "HospitalManagementSystem.exe")
        print("✓ Main executable copied")
    else:
        print("✗ Main executable not found")
        return False
    
    # Step 2: Copy source files
    print("\nStep 2: Copying source files...")
    source_files = [
        "desktop_app.py",
        "patient_management.py",
        "appointment_management.py",
        "billing_management.py",
        "lab_management.py",
        "reports_management.py",
        "user_management.py",
        "launch.py",
        "requirements.txt",
        "README.md",
        "LOGIN_CREDENTIALS.txt"
    ]
    
    for file_name in source_files:
        source_file = current_dir / file_name
        if source_file.exists():
            shutil.copy2(source_file, package_dir / file_name)
            print(f"  Copied: {file_name}")
    
    # Step 3: Create installation scripts
    print("\nStep 3: Creating installation scripts...")
    create_installation_scripts(package_dir)
    
    # Step 4: Create documentation
    print("\nStep 4: Creating documentation...")
    create_package_documentation(package_dir, app_name, app_version)
    
    # Step 5: Create zip package
    print("\nStep 5: Creating zip package...")
    zip_path = dist_dir / package_name
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
                print(f"  Added to package: {arcname}")
    
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"✓ Package created: {zip_path}")
    print(f"  Size: {size_mb:.1f} MB")
    
    return True

def create_installation_scripts(package_dir):
    """Create installation and setup scripts"""
    
    # Quick install script
    quick_install = """@echo off
title Hospital Management System - Quick Install

echo.
echo ================================================================
echo  Hospital Management System - Quick Install
echo  Publisher: Kaitsnet IT Solutions
echo  Version: 1.0.0
echo ================================================================
echo.

echo Starting Hospital Management System...
echo.

REM Check if executable exists
if not exist "HospitalManagementSystem.exe" (
    echo ERROR: HospitalManagementSystem.exe not found!
    echo Please ensure all files are extracted to the same folder.
    echo.
    pause
    exit /b 1
)

REM Start the application
start "" "HospitalManagementSystem.exe"

echo.
echo Application started successfully!
echo.
echo Default login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo IMPORTANT: Change the default password after first login!
echo.
pause
"""
    
    with open(package_dir / "QUICK_INSTALL.bat", 'w') as f:
        f.write(quick_install)
    
    # Full install script
    full_install = """@echo off
title Hospital Management System - Full Install

echo.
echo ================================================================
echo  Hospital Management System - Full Install
echo  Publisher: Kaitsnet IT Solutions
echo  Version: 1.0.0
echo ================================================================
echo.

echo Installing Hospital Management System...
echo.

REM Create installation directory
set INSTALL_DIR=%PROGRAMFILES%\\HospitalManagementSystem
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
copy "HospitalManagementSystem.exe" "%INSTALL_DIR%\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Hospital Management System.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\HospitalManagementSystem.exe'; $Shortcut.Save()"

REM Create start menu shortcut
echo Creating start menu shortcut...
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Hospital Management System" mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Hospital Management System"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Hospital Management System\\Hospital Management System.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\HospitalManagementSystem.exe'; $Shortcut.Save()"

echo.
echo ================================================================
echo  Installation completed successfully!
echo ================================================================
echo.
echo The application has been installed to:
echo   %INSTALL_DIR%
echo.
echo Desktop and Start Menu shortcuts have been created.
echo.
echo Default login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo IMPORTANT: Change the default password after first login!
echo.
pause
"""
    
    with open(package_dir / "FULL_INSTALL.bat", 'w') as f:
        f.write(full_install)
    
    # Setup script for Python development
    setup_script = """@echo off
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
    pause
    exit /b 1
)

echo Python detected. Installing dependencies...
echo.

REM Install required packages
python -m pip install --upgrade pip
python -m pip install tkcalendar==1.6.1 matplotlib pandas Pillow

echo.
echo ================================================================
echo  Setup completed successfully!
echo ================================================================
echo.
echo You can now run the application using: python launch.py
echo.
pause
"""
    
    with open(package_dir / "SETUP.bat", 'w') as f:
        f.write(setup_script)
    
    # Run script for Python development
    run_script = """@echo off
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
    echo Please run SETUP.bat first to install dependencies
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
"""
    
    with open(package_dir / "RUN_APP.bat", 'w') as f:
        f.write(run_script)
    
    print("  Created: QUICK_INSTALL.bat, FULL_INSTALL.bat, SETUP.bat, RUN_APP.bat")

def create_package_documentation(package_dir, app_name, app_version):
    """Create comprehensive package documentation"""
    
    readme_content = f"""Hospital Management System - Complete Installation Package
===============================================================

Version: {app_version}
Publisher: Kaitsnet IT Solutions
Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW
--------

This package contains everything needed to install and run the Hospital Management System
on Windows systems. Choose the installation method that best suits your needs.

INSTALLATION METHODS
-------------------

Method 1: Quick Install (Recommended for End Users)
1. Extract all files to a folder
2. Double-click: QUICK_INSTALL.bat
3. The application will start immediately
4. Login with: admin / admin123

Method 2: Full Install (System-wide Installation)
1. Extract all files to a folder
2. Run as Administrator: FULL_INSTALL.bat
3. Application will be installed to Program Files
4. Desktop and Start Menu shortcuts will be created
5. Login with: admin / admin123

Method 3: Python Development (For Developers)
1. Extract all files to a folder
2. Run: SETUP.bat (installs Python dependencies)
3. Run: RUN_APP.bat (starts the application)
4. Login with: admin / admin123

SYSTEM REQUIREMENTS
------------------

- Windows 10 or later
- Python 3.7 or higher (for development method)
- 4GB RAM minimum
- 100MB free disk space
- 1366x768 minimum resolution

FEATURES
--------

✓ Patient Management
✓ Appointment Scheduling
✓ Billing Management
✓ Lab Test Management
✓ User Management
✓ Reports and Analytics
✓ Modern Dark Theme UI
✓ Role-based Access Control
✓ Database Management
✓ Export and Reporting

DEFAULT LOGIN CREDENTIALS
------------------------

Username: admin
Password: admin123

IMPORTANT SECURITY NOTES:
- Change the default password immediately after first login
- Use strong passwords in production environments
- Create additional user accounts for staff members
- Never share admin credentials

USER ROLES
----------

Admin:
- Full system access
- User management
- System configuration
- Reports and analytics

Doctor:
- Patient management
- Appointment scheduling
- Medical records
- Lab test management

Staff:
- Basic patient access
- Appointment viewing
- Limited functionality

PACKAGE CONTENTS
----------------

Executables:
- HospitalManagementSystem.exe - Main application

Installation Scripts:
- QUICK_INSTALL.bat - Quick start (recommended)
- FULL_INSTALL.bat - System-wide installation
- SETUP.bat - Python development setup
- RUN_APP.bat - Python development run

Source Files:
- desktop_app.py - Main application
- patient_management.py - Patient management module
- appointment_management.py - Appointment management
- billing_management.py - Billing management
- lab_management.py - Lab test management
- reports_management.py - Reports and analytics
- user_management.py - User management
- launch.py - Application launcher
- requirements.txt - Python dependencies

Documentation:
- README.md - Main documentation
- LOGIN_CREDENTIALS.txt - Login information
- This file - Installation guide

TROUBLESHOOTING
--------------

Common Issues:

1. "Application won't start"
   Solution: Try QUICK_INSTALL.bat or check system requirements

2. "Python not found" (for development)
   Solution: Install Python 3.7+ from python.org

3. "Missing dependencies" (for development)
   Solution: Run SETUP.bat to install automatically

4. "Login failed"
   Solution: Use default credentials: admin / admin123

5. "Permission denied"
   Solution: Run FULL_INSTALL.bat as Administrator

SUPPORT
-------

For technical support:
- Email: support@kaitsnet.com
- Website: https://www.kaitsnet.com/support
- Documentation: README.md

LICENSE
-------

This software is licensed for use in healthcare facilities.
See LICENSE.txt for complete terms and conditions.

© 2024 Kaitsnet IT Solutions. All rights reserved.

QUICK START GUIDE
----------------

For immediate use:
1. Extract all files to a folder
2. Double-click QUICK_INSTALL.bat
3. Login with admin / admin123
4. Start managing your hospital!

For system-wide installation:
1. Extract all files to a folder
2. Right-click FULL_INSTALL.bat → "Run as Administrator"
3. Follow the installation prompts
4. Use desktop or start menu shortcuts
5. Login with admin / admin123
"""
    
    with open(package_dir / "INSTALLATION_GUIDE.txt", 'w') as f:
        f.write(readme_content)
    
    print("  Created: INSTALLATION_GUIDE.txt")

def main():
    """Main function"""
    success = create_installation_package()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ COMPLETE INSTALLATION PACKAGE CREATED SUCCESSFULLY!")
        print("=" * 60)
        print("The package includes everything needed for installation.")
        print("Users can choose from multiple installation methods.")
        print("\nPackage includes:")
        print("- Standalone executable")
        print("- Multiple installation scripts")
        print("- Complete source code")
        print("- Comprehensive documentation")
        print("- Quick start guides")
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ PACKAGE CREATION FAILED!")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    exit(main()) 