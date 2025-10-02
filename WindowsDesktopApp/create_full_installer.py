#!/usr/bin/env python3
"""
Hospital Management System - Full Windows Installer Creator
Creates a complete Windows installation package
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_full_installer():
    """Create a complete Windows installation package"""
    print("Hospital Management System - Full Installer Creator")
    print("=" * 60)
    
    # Configuration
    app_name = "Hospital Management System"
    app_version = "1.0.0"
    installer_name = f"HospitalManagementSystem_v{app_version}_Full_Setup.exe"
    package_name = f"HospitalManagementSystem_v{app_version}_Full_Package.zip"
    
    # Directories
    current_dir = Path(__file__).parent
    build_dir = current_dir / "build"
    dist_dir = current_dir / "dist"
    package_dir = dist_dir / "package"
    
    # Create directories
    build_dir.mkdir(exist_ok=True)
    dist_dir.mkdir(exist_ok=True)
    package_dir.mkdir(exist_ok=True)
    
    print(f"Building {app_name} v{app_version}")
    print(f"Output: {dist_dir / installer_name}")
    
    # Step 1: Build the main executable
    print("\nStep 1: Building main executable...")
    success = build_main_executable(current_dir, build_dir, dist_dir, installer_name)
    if not success:
        return False
    
    # Step 2: Create installation package
    print("\nStep 2: Creating installation package...")
    success = create_installation_package(current_dir, dist_dir, package_dir, package_name)
    if not success:
        return False
    
    # Step 3: Create installation scripts
    print("\nStep 3: Creating installation scripts...")
    create_installation_scripts(dist_dir, installer_name)
    
    # Step 4: Create documentation
    print("\nStep 4: Creating documentation...")
    create_installation_documentation(dist_dir, installer_name)
    
    return True

def build_main_executable(current_dir, build_dir, dist_dir, installer_name):
    """Build the main executable using PyInstaller"""
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "HospitalManagementSystem",
        "--distpath", str(dist_dir),
        "--workpath", str(build_dir),
        "--specpath", str(build_dir),
        "--clean",
        "--noconfirm",
        str(current_dir / "desktop_app.py")
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Main executable built successfully")
            
            # Check if executable was created
            exe_path = dist_dir / "HospitalManagementSystem.exe"
            if exe_path.exists():
                # Rename to installer name
                installer_path = dist_dir / installer_name
                shutil.move(str(exe_path), str(installer_path))
                
                size_mb = installer_path.stat().st_size / (1024 * 1024)
                print(f"  File: {installer_path}")
                print(f"  Size: {size_mb:.1f} MB")
                return True
            else:
                print("✗ Executable not found after build")
                return False
        else:
            print("✗ PyInstaller build failed:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Build process failed: {e}")
        return False

def create_installation_package(current_dir, dist_dir, package_dir, package_name):
    """Create a complete installation package"""
    # Files to include in the package
    files_to_include = [
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
    
    # Copy files to package directory
    for file_name in files_to_include:
        source_file = current_dir / file_name
        if source_file.exists():
            dest_file = package_dir / file_name
            shutil.copy2(source_file, dest_file)
            print(f"  Copied: {file_name}")
    
    # Create batch files for easy execution
    create_batch_files(package_dir)
    
    # Create zip package
    zip_path = dist_dir / package_name
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"✓ Package created: {zip_path}")
    print(f"  Size: {size_mb:.1f} MB")
    
    return True

def create_batch_files(package_dir):
    """Create batch files for easy execution"""
    # Setup batch file
    setup_bat = """@echo off
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
echo You can now run the application using: run_app.bat
echo.
pause
"""
    
    with open(package_dir / "setup.bat", 'w') as f:
        f.write(setup_bat)
    
    # Run app batch file
    run_app_bat = """@echo off
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
    echo Please run setup.bat first to install dependencies
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
    
    with open(package_dir / "run_app.bat", 'w') as f:
        f.write(run_app_bat)
    
    print("  Created: setup.bat, run_app.bat")

def create_installation_scripts(dist_dir, installer_name):
    """Create installation scripts"""
    # Installation script
    install_script = f"""@echo off
title Hospital Management System - Installation

echo.
echo ================================================================
echo  Hospital Management System - Installation
echo  Publisher: Kaitsnet IT Solutions
echo  Version: 1.0.0
echo ================================================================
echo.

echo Installing Hospital Management System...
echo.

REM Create installation directory
set INSTALL_DIR=%PROGRAMFILES%\\HospitalManagementSystem
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
copy "{installer_name}" "%INSTALL_DIR%\\"
copy "README_INSTALLER.txt" "%INSTALL_DIR%\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Hospital Management System.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{installer_name}'; $Shortcut.Save()"

REM Create start menu shortcut
echo Creating start menu shortcut...
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Hospital Management System" mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Hospital Management System"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Hospital Management System\\Hospital Management System.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{installer_name}'; $Shortcut.Save()"

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
    
    with open(dist_dir / "install.bat", 'w') as f:
        f.write(install_script)
    
    print("  Created: install.bat")

def create_installation_documentation(dist_dir, installer_name):
    """Create comprehensive installation documentation"""
    readme_content = f"""Hospital Management System - Windows Installation Guide
========================================================

Version: 1.0.0
Publisher: Kaitsnet IT Solutions
Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW
--------

This package contains a complete Windows installation for the Hospital Management System.
The application is a professional healthcare management solution with modern UI.

INSTALLATION OPTIONS
-------------------

Option 1: Quick Install (Recommended)
1. Run: {installer_name}
2. The application will start immediately
3. Login with: admin / admin123

Option 2: Full Installation
1. Run: install.bat
2. Follow the installation prompts
3. Use desktop/start menu shortcuts
4. Login with: admin / admin123

Option 3: Manual Setup
1. Run: setup.bat (installs dependencies)
2. Run: run_app.bat (starts application)
3. Login with: admin / admin123

SYSTEM REQUIREMENTS
------------------

- Windows 10 or later
- Python 3.7 or higher (for manual setup)
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

Doctor:
- Patient management
- Appointment scheduling
- Medical records

Staff:
- Basic patient access
- Appointment viewing
- Limited functionality

TROUBLESHOOTING
--------------

Common Issues:

1. "Python not found"
   Solution: Install Python 3.7+ from python.org

2. "Missing dependencies"
   Solution: Run setup.bat to install automatically

3. "Application won't start"
   Solution: Check if all files are present and run setup.bat

4. "Login failed"
   Solution: Use default credentials: admin / admin123

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

PACKAGE CONTENTS
----------------

- {installer_name} - Main application executable
- install.bat - Installation script
- README_INSTALLER.txt - This file
- HospitalManagementSystem_v1.0.0_Full_Package.zip - Source code package

For developers or advanced users, the source code package contains:
- All Python source files
- Setup scripts
- Documentation
- Requirements file
"""
    
    readme_file = dist_dir / "README_INSTALLER.txt"
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    
    print("  Created: README_INSTALLER.txt")

def main():
    """Main function"""
    success = create_full_installer()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ FULL INSTALLER PACKAGE CREATED SUCCESSFULLY!")
        print("=" * 60)
        print("The complete installation package is ready for distribution.")
        print("Users can install and run the application on any Windows 10+ system.")
        print("\nPackage includes:")
        print("- Standalone executable installer")
        print("- Complete source code package")
        print("- Installation scripts")
        print("- Comprehensive documentation")
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ INSTALLER PACKAGE CREATION FAILED!")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    exit(main()) 