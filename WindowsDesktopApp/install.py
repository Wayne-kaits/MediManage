#!/usr/bin/env python3
"""
Hospital Management System - Desktop Application Installer
Advanced version with all dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required Python packages"""
    print("Installing required packages...")
    
    packages = [
        "tkcalendar==1.6.1",
        "matplotlib==3.7.2",
        "pandas==2.0.3",
        "Pillow==10.0.0"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            return False
    
    return True

def create_data_directory():
    """Create data directory for database"""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    print(f"✓ Data directory created: {data_dir}")

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if os.name != 'nt':
        return
        
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Hospital Management System.lnk")
        target = os.path.join(os.path.dirname(__file__), "start_hospital_app.bat")
        wDir = os.path.dirname(__file__)
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = target
        shortcut.save()
        
        print(f"✓ Desktop shortcut created: {path}")
    except ImportError:
        print("! Desktop shortcut creation skipped (winshell not available)")
    except Exception as e:
        print(f"! Desktop shortcut creation failed: {e}")

def create_batch_file():
    """Create batch file to start the application"""
    batch_content = f'''@echo off
cd /d "{os.path.dirname(__file__)}"
python desktop_app.py
pause
'''
    
    batch_path = os.path.join(os.path.dirname(__file__), "start_hospital_app.bat")
    with open(batch_path, 'w') as f:
        f.write(batch_content)
    
    print(f"✓ Batch file created: {batch_path}")

def main():
    """Main installer function"""
    print("Hospital Management System - Advanced Desktop Application Installer")
    print("=" * 70)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not install_dependencies():
        print("\nInstallation failed!")
        input("Press Enter to exit...")
        return
    
    # Create data directory
    create_data_directory()
    
    # Create batch file
    create_batch_file()
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    print("\n" + "=" * 70)
    print("Installation completed successfully!")
    print("\nAdvanced Features Included:")
    print("• Modern Dark Theme UI")
    print("• Patient Management with Medical History")
    print("• Advanced Appointment Scheduling")
    print("• Comprehensive Billing System")
    print("• Lab Test Management with Results")
    print("• Reports & Analytics with Charts")
    print("• User Management (Admin)")
    print("• Role-based Access Control")
    print("• Data Export Capabilities")
    
    print("\nYou can now run the application by:")
    print("1. Double-clicking 'start_hospital_app.bat'")
    print("2. Running 'python desktop_app.py'")
    
    if os.name == 'nt':
        print("3. Using the desktop shortcut (if created)")
    
    print("\nDefault login credentials:")
    print("Username: admin")
    print("Password: admin123")
    
    print("\nSystem Requirements:")
    print("• Python 3.7 or higher")
    print("• Windows 10 or higher")
    print("• 4GB RAM minimum")
    print("• 100MB free disk space")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()