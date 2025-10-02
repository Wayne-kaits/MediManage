#!/usr/bin/env python3
"""
Hospital Management System - Simple Installer Creator
Creates a standalone Windows executable installer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_installer():
    """Create a standalone Windows installer"""
    print("Hospital Management System - Installer Creator")
    print("=" * 50)
    
    # Configuration
    app_name = "Hospital Management System"
    app_version = "1.0.0"
    installer_name = f"HospitalManagementSystem_v{app_version}_Setup.exe"
    
    # Directories
    current_dir = Path(__file__).parent
    build_dir = current_dir / "build"
    dist_dir = current_dir / "dist"
    
    # Create directories
    build_dir.mkdir(exist_ok=True)
    dist_dir.mkdir(exist_ok=True)
    
    print(f"Building {app_name} v{app_version}")
    print(f"Output: {dist_dir / installer_name}")
    
    # PyInstaller command for desktop_app.py
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
        print("Running PyInstaller...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ PyInstaller build successful")
            
            # Check if executable was created
            exe_path = dist_dir / "HospitalManagementSystem.exe"
            if exe_path.exists():
                # Rename to installer name
                installer_path = dist_dir / installer_name
                shutil.move(str(exe_path), str(installer_path))
                
                size_mb = installer_path.stat().st_size / (1024 * 1024)
                print(f"✓ Installer created successfully!")
                print(f"  File: {installer_path}")
                print(f"  Size: {size_mb:.1f} MB")
                
                # Create README for installer
                create_installer_readme(dist_dir, installer_name)
                
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

def create_installer_readme(dist_dir, installer_name):
    """Create README for the installer"""
    readme_content = f"""Hospital Management System - Windows Installer
=====================================

Version: 1.0.0
Publisher: Kaitsnet IT Solutions

INSTALLATION INSTRUCTIONS
-------------------------

1. Run the installer: {installer_name}
2. The application will start automatically
3. Login with default credentials:
   Username: admin
   Password: admin123
4. Change the default password immediately

SYSTEM REQUIREMENTS
------------------

- Windows 10 or later
- 4GB RAM minimum
- 100MB free disk space
- 1366x768 minimum resolution

FEATURES
--------

- Patient Management
- Appointment Scheduling
- Billing Management
- Lab Test Management
- User Management
- Reports and Analytics

DEFAULT LOGIN
------------

Username: admin
Password: admin123

IMPORTANT: Change the default password after first login!

SUPPORT
-------

For technical support:
- Email: support@kaitsnet.com
- Website: https://www.kaitsnet.com/support

© 2024 Kaitsnet IT Solutions. All rights reserved.
"""
    
    readme_file = dist_dir / "README_INSTALLER.txt"
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    
    print(f"✓ README created: {readme_file}")

def main():
    """Main function"""
    success = create_installer()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ INSTALLER CREATED SUCCESSFULLY!")
        print("=" * 50)
        print("The installer is ready for distribution.")
        print("Users can run it directly on any Windows 10+ system.")
        return 0
    else:
        print("\n" + "=" * 50)
        print("❌ INSTALLER CREATION FAILED!")
        print("=" * 50)
        return 1

if __name__ == "__main__":
    exit(main()) 