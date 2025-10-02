#!/usr/bin/env python3
"""
Hospital Management System - Professional EXE Creator
Creates a professional Windows executable with custom icon and branding
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def create_professional_icon():
    """Create a professional medical icon"""
    print("Creating professional medical icon...")
    
    try:
        # Create a professional medical icon
        size = 256
        icon = Image.new('RGBA', (size, size), (0, 123, 255, 255))  # Professional blue
        
        # Create a medical cross design
        draw = ImageDraw.Draw(icon)
        
        # Draw a professional medical cross
        cross_width = size // 6
        cross_height = size // 2
        
        # Vertical line (main cross)
        x1 = (size - cross_width) // 2
        y1 = (size - cross_height) // 2
        x2 = x1 + cross_width
        y2 = y1 + cross_height
        draw.rectangle([x1, y1, x2, y2], fill='white')
        
        # Horizontal line
        h_x1 = (size - cross_height) // 2
        h_y1 = (size - cross_width) // 2
        h_x2 = h_x1 + cross_height
        h_y2 = h_y1 + cross_width
        draw.rectangle([h_x1, h_y1, h_x2, h_y2], fill='white')
        
        # Add a subtle border
        border_color = (255, 255, 255, 100)
        draw.rectangle([0, 0, size-1, size-1], outline=border_color, width=3)
        
        # Save as ICO with multiple sizes
        icon_path = Path(__file__).parent / "hospital_icon.ico"
        icon.save(icon_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        
        print(f"✓ Professional icon created: {icon_path}")
        return icon_path
        
    except Exception as e:
        print(f"✗ Icon creation failed: {e}")
        return None

def create_version_file():
    """Create a professional version info file"""
    print("Creating version info file...")
    
    version_content = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Kaitsnet IT Solutions'),
        StringStruct(u'FileDescription', u'Hospital Management System - Professional Healthcare Management Solution'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'HospitalManagementSystem'),
        StringStruct(u'LegalCopyright', u'© 2024 Kaitsnet IT Solutions. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'HospitalManagementSystem.exe'),
        StringStruct(u'ProductName', u'Hospital Management System'),
        StringStruct(u'ProductVersion', u'1.0.0'),
        StringStruct(u'Comments', u'Professional hospital management solution for healthcare facilities'),
        StringStruct(u'LegalTrademarks', u'Hospital Management System is a trademark of Kaitsnet IT Solutions')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
    
    version_file = Path(__file__).parent / "version_info.txt"
    with open(version_file, 'w') as f:
        f.write(version_content)
    
    print(f"✓ Version file created: {version_file}")
    return version_file

def build_professional_executable():
    """Build a professional Windows executable"""
    print("Building professional Windows executable...")
    
    current_dir = Path(__file__).parent
    build_dir = current_dir / "build"
    dist_dir = current_dir / "dist"
    
    # Create directories
    build_dir.mkdir(exist_ok=True)
    dist_dir.mkdir(exist_ok=True)
    
    # Create icon and version file
    icon_path = create_professional_icon()
    version_file = create_version_file()
    
    # PyInstaller command with professional settings
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
        "--uac-admin",  # Request admin privileges
        "--version-file", str(version_file)
    ]
    
    # Add icon if created successfully
    if icon_path:
        cmd.extend(["--icon", str(icon_path)])
    
    # Add the main application file
    cmd.append(str(current_dir / "desktop_app.py"))
    
    try:
        print("Running PyInstaller with professional settings...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Professional executable built successfully")
            
            # Check if executable was created
            exe_path = dist_dir / "HospitalManagementSystem.exe"
            if exe_path.exists():
                # Rename to professional name
                professional_name = "HospitalManagementSystem_Professional.exe"
                professional_path = dist_dir / professional_name
                shutil.move(str(exe_path), str(professional_path))
                
                size_mb = professional_path.stat().st_size / (1024 * 1024)
                print(f"✓ Professional executable created: {professional_path}")
                print(f"  Size: {size_mb:.1f} MB")
                print(f"  Icon: {'✓ Custom medical icon' if icon_path else '✗ Default icon'}")
                print(f"  Version: ✓ Professional version info")
                print(f"  UAC: ✓ Admin privileges requested")
                
                return professional_path
            else:
                print("✗ Executable not found after build")
                return None
        else:
            print("✗ PyInstaller build failed:")
            print(result.stdout)
            print(result.stderr)
            return None
            
    except Exception as e:
        print(f"✗ Build process failed: {e}")
        return None

def create_professional_installer():
    """Create a professional installer package"""
    print("Creating professional installer package...")
    
    current_dir = Path(__file__).parent
    dist_dir = current_dir / "dist"
    installer_dir = dist_dir / "professional_installer"
    
    # Create installer directory
    installer_dir.mkdir(exist_ok=True)
    
    # Build the professional executable
    exe_path = build_professional_executable()
    if not exe_path:
        return False
    
    # Copy executable to installer directory
    installer_exe = installer_dir / "HospitalManagementSystem.exe"
    shutil.copy2(exe_path, installer_exe)
    
    # Create professional installation script
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
copy "HospitalManagementSystem.exe" "%INSTALL_DIR%\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Hospital Management System.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\HospitalManagementSystem.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\\HospitalManagementSystem.exe,0'; $Shortcut.Save()"

REM Create start menu shortcut
echo Creating start menu shortcut...
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Kaitsnet" mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Kaitsnet"
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Kaitsnet\\Hospital Management System" mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Kaitsnet\\Hospital Management System"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Kaitsnet\\Hospital Management System\\Hospital Management System.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\HospitalManagementSystem.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\\HospitalManagementSystem.exe,0'; $Shortcut.Save()"

REM Register in Programs and Features
echo Registering application...
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\HospitalManagementSystem" /v "DisplayName" /t REG_SZ /d "Hospital Management System" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\HospitalManagementSystem" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\\uninstall.exe" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\HospitalManagementSystem" /v "DisplayIcon" /t REG_SZ /d "%INSTALL_DIR%\\HospitalManagementSystem.exe" /f
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
    
    with open(installer_dir / "INSTALL_PROFESSIONAL.bat", 'w') as f:
        f.write(install_script)
    
    # Create professional README
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
and reporting capabilities.

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

INSTALLATION
------------

1. Run INSTALL_PROFESSIONAL.bat as Administrator
2. Follow the installation prompts
3. Use desktop or start menu shortcuts
4. Login with: admin / admin123

SYSTEM REQUIREMENTS
------------------

- Windows 10 or later
- 4GB RAM minimum
- 100MB free disk space
- 1366x768 minimum resolution

DEFAULT LOGIN
------------

Username: admin
Password: admin123

IMPORTANT: Change the default password after first login!

SUPPORT
-------

For professional support:
- Email: support@kaitsnet.com
- Website: https://www.kaitsnet.com/support
- Phone: +1-800-KAITSNET

© 2024 Kaitsnet IT Solutions. All rights reserved.
"""
    
    with open(installer_dir / "README_PROFESSIONAL.txt", 'w') as f:
        f.write(readme_content)
    
    print(f"✓ Professional installer package created: {installer_dir}")
    return True

def main():
    """Main function"""
    print("Hospital Management System - Professional EXE Creator")
    print("=" * 60)
    
    success = create_professional_installer()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ PROFESSIONAL EXECUTABLE CREATED SUCCESSFULLY!")
        print("=" * 60)
        print("The professional executable is ready for distribution.")
        print("Features:")
        print("- Custom medical icon")
        print("- Professional version information")
        print("- UAC admin privileges")
        print("- Professional installation package")
        print("- Trustworthy branding")
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ PROFESSIONAL EXECUTABLE CREATION FAILED!")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    exit(main()) 