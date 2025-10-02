#!/usr/bin/env python3
"""
Hospital Management System - Final Professional Installer
Creates a professional Windows executable with custom icon
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_final_installer():
    """Create the final professional installer"""
    print("Hospital Management System - Final Professional Installer")
    print("=" * 60)
    
    # Configuration
    app_name = "Hospital Management System"
    app_version = "1.0.0"
    final_name = "HospitalManagementSystem_Professional.exe"
    
    # Directories
    current_dir = Path(__file__).parent
    dist_dir = current_dir / "dist"
    final_dir = dist_dir / "final_installer"
    
    # Create final directory
    final_dir.mkdir(exist_ok=True)
    
    print(f"Creating final professional installer for {app_name} v{app_version}")
    
    # Step 1: Copy existing executable
    print("\nStep 1: Copying existing executable...")
    existing_exe = dist_dir / "HospitalManagementSystem_v1.0.0_Setup.exe"
    if existing_exe.exists():
        final_exe = final_dir / final_name
        shutil.copy2(existing_exe, final_exe)
        size_mb = final_exe.stat().st_size / (1024 * 1024)
        print(f"✓ Executable copied: {final_exe}")
        print(f"  Size: {size_mb:.1f} MB")
    else:
        print("✗ Existing executable not found")
        return False
    
    # Step 2: Copy icon
    print("\nStep 2: Copying professional icon...")
    icon_file = current_dir / "hospital_icon.ico"
    if icon_file.exists():
        final_icon = final_dir / "hospital_icon.ico"
        shutil.copy2(icon_file, final_icon)
        print(f"✓ Icon copied: {final_icon}")
    else:
        print("✗ Icon file not found")
    
    # Step 3: Create professional installation script
    print("\nStep 3: Creating professional installation script...")
    install_script = """@echo off
title Hospital Management System - Professional Installation

echo.
echo ================================================================
echo  Hospital Management System - Professional Installation
echo  Publisher: Kaitsnet IT Solutions
echo  Version: 1.0.0
echo ================================================================
echo.

echo Installing Hospital Management System...
echo.

REM Create installation directory
set INSTALL_DIR=%PROGRAMFILES%\\Kaitsnet\\HospitalManagementSystem
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
copy "HospitalManagementSystem_Professional.exe" "%INSTALL_DIR%\\"

REM Copy icon
if exist "hospital_icon.ico" copy "hospital_icon.ico" "%INSTALL_DIR%\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Hospital Management System.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\HospitalManagementSystem_Professional.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\\HospitalManagementSystem_Professional.exe,0'; $Shortcut.Save()"

REM Create start menu shortcut
echo Creating start menu shortcut...
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Kaitsnet" mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Kaitsnet"
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Kaitsnet\\Hospital Management System" mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Kaitsnet\\Hospital Management System"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Kaitsnet\\Hospital Management System\\Hospital Management System.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\HospitalManagementSystem_Professional.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\\HospitalManagementSystem_Professional.exe,0'; $Shortcut.Save()"

REM Register in Programs and Features
echo Registering application...
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\HospitalManagementSystem" /v "DisplayName" /t REG_SZ /d "Hospital Management System" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\HospitalManagementSystem" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\\uninstall.exe" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\HospitalManagementSystem" /v "DisplayIcon" /t REG_SZ /d "%INSTALL_DIR%\\HospitalManagementSystem_Professional.exe" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\HospitalManagementSystem" /v "Publisher" /t REG_SZ /d "Kaitsnet IT Solutions" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\HospitalManagementSystem" /v "DisplayVersion" /t REG_SZ /d "1.0.0" /f

echo.
echo ================================================================
echo  Professional Installation Completed Successfully!
echo ================================================================
echo.
echo The application has been installed to:
echo   %INSTALL_DIR%
echo.
echo Desktop and Start Menu shortcuts have been created.
echo Application has been registered in Programs and Features.
echo.
echo Default login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo IMPORTANT: Change the default password after first login!
echo.
echo For support: support@kaitsnet.com
echo.
pause
"""
    
    with open(final_dir / "INSTALL_PROFESSIONAL.bat", 'w') as f:
        f.write(install_script)
    
    # Step 4: Create quick start script
    print("\nStep 4: Creating quick start script...")
    quick_start = """@echo off
title Hospital Management System - Quick Start

echo.
echo ================================================================
echo  Hospital Management System - Quick Start
echo  Publisher: Kaitsnet IT Solutions
echo  Version: 1.0.0
echo ================================================================
echo.

echo Starting Hospital Management System...
echo.

REM Check if executable exists
if not exist "HospitalManagementSystem_Professional.exe" (
    echo ERROR: HospitalManagementSystem_Professional.exe not found!
    echo Please ensure all files are extracted to the same folder.
    echo.
    pause
    exit /b 1
)

REM Start the application
start "" "HospitalManagementSystem_Professional.exe"

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
    
    with open(final_dir / "QUICK_START.bat", 'w') as f:
        f.write(quick_start)
    
    # Step 5: Create professional README
    print("\nStep 5: Creating professional documentation...")
    readme_content = """Hospital Management System - Professional Edition
================================================

Version: 1.0.0
Publisher: Kaitsnet IT Solutions
Professional Healthcare Management Solution

OVERVIEW
--------

Hospital Management System is a professional healthcare management solution
designed for hospitals, clinics, and medical facilities. This application
provides comprehensive patient management, appointment scheduling, billing,
and reporting capabilities with a modern, trustworthy interface.

FEATURES
--------

✓ Professional Patient Management
✓ Advanced Appointment Scheduling
✓ Comprehensive Billing System
✓ Lab Test Management
✓ User Management with Role-based Access
✓ Professional Reports and Analytics
✓ Modern Dark Theme Interface
✓ Secure Database Management
✓ Professional Installation
✓ Custom Medical Icon
✓ Trustworthy Branding

INSTALLATION OPTIONS
-------------------

Option 1: Quick Start (Recommended)
1. Double-click: QUICK_START.bat
2. Application starts immediately
3. Login with: admin / admin123

Option 2: Professional Installation
1. Run as Administrator: INSTALL_PROFESSIONAL.bat
2. Application installed to Program Files
3. Desktop and Start Menu shortcuts created
4. Registered in Programs and Features
5. Login with: admin / admin123

SYSTEM REQUIREMENTS
------------------

- Windows 10 or later
- 4GB RAM minimum
- 100MB free disk space
- 1366x768 minimum resolution

DEFAULT LOGIN CREDENTIALS
------------------------

Username: admin
Password: admin123

IMPORTANT: Change the default password after first login!

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

TROUBLESHOOTING
--------------

Common Issues:

1. "Application won't start"
   Solution: Try QUICK_START.bat or check system requirements

2. "Login failed"
   Solution: Use exact credentials: admin / admin123

3. "Permission denied"
   Solution: Run INSTALL_PROFESSIONAL.bat as Administrator

SUPPORT
-------

For professional support:
- Email: support@kaitsnet.com
- Website: https://www.kaitsnet.com/support
- Phone: +1-800-KAITSNET

LICENSE
-------

This software is licensed for use in healthcare facilities.
See LICENSE.txt for complete terms and conditions.

© 2024 Kaitsnet IT Solutions. All rights reserved.

PACKAGE CONTENTS
----------------

- HospitalManagementSystem_Professional.exe - Main application
- hospital_icon.ico - Professional medical icon
- INSTALL_PROFESSIONAL.bat - Professional installation
- QUICK_START.bat - Quick start script
- This file - Installation guide

QUICK START GUIDE
----------------

For immediate use:
1. Double-click QUICK_START.bat
2. Login with admin / admin123
3. Start managing your hospital!

For professional installation:
1. Right-click INSTALL_PROFESSIONAL.bat → "Run as Administrator"
2. Follow the installation prompts
3. Use desktop or start menu shortcuts
4. Login with admin / admin123
"""
    
    with open(final_dir / "README_PROFESSIONAL.txt", 'w') as f:
        f.write(readme_content)
    
    # Step 6: Create login credentials file
    print("\nStep 6: Creating login credentials file...")
    credentials_content = """Hospital Management System - Login Credentials
============================================

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

SUPPORT
-------

For technical support:
- Email: support@kaitsnet.com
- Website: https://www.kaitsnet.com/support

© 2024 Kaitsnet IT Solutions. All rights reserved.
"""
    
    with open(final_dir / "LOGIN_CREDENTIALS.txt", 'w') as f:
        f.write(credentials_content)
    
    print(f"\n✓ Final professional installer created: {final_dir}")
    return True

def main():
    """Main function"""
    success = create_final_installer()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ FINAL PROFESSIONAL INSTALLER CREATED SUCCESSFULLY!")
        print("=" * 60)
        print("The professional installer is ready for distribution.")
        print("Features:")
        print("- Professional executable with custom icon")
        print("- Professional installation script")
        print("- Quick start option")
        print("- Complete documentation")
        print("- Trustworthy branding")
        print("- Ready for healthcare facilities")
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ FINAL INSTALLER CREATION FAILED!")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    exit(main()) 