#!/usr/bin/env python3
"""
Hospital Management System - Desktop Application Launcher
Quick launcher with dependency checking
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'tkinter',
        'tkcalendar',
        'matplotlib',
        'pandas',
        'PIL'  # Pillow
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_missing_packages(packages):
    """Install missing packages"""
    print("Installing missing packages...")
    
    package_map = {
        'PIL': 'Pillow==10.0.0',
        'tkcalendar': 'tkcalendar==1.6.1',
        'matplotlib': 'matplotlib==3.7.2',
        'pandas': 'pandas==2.0.3'
    }
    
    success_count = 0
    
    for package in packages:
        if package == 'tkinter':
            print(f"⚠️  {package} is not available. Please install Python with tkinter support.")
            continue
            
        install_name = package_map.get(package, package)
        try:
            print(f"Installing {install_name}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", install_name], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✓ {install_name} installed successfully")
                success_count += 1
            else:
                print(f"✗ Failed to install {install_name}: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"✗ Installation of {install_name} timed out")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {install_name}: {e}")
        except Exception as e:
            print(f"✗ Unexpected error installing {install_name}: {e}")
    
    return success_count == len([p for p in packages if p != 'tkinter'])

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_application_files():
    """Check if all required application files exist"""
    required_files = [
        "desktop_app.py",
        "patient_management.py",
        "appointment_management.py", 
        "billing_management.py",
        "lab_management.py",
        "reports_management.py",
        "user_management.py"
    ]
    
    missing_files = []
    for file_name in required_files:
        file_path = Path(__file__).parent / file_name
        if not file_path.exists():
            missing_files.append(file_name)
    
    if missing_files:
        print("❌ Error: Missing required application files:")
        for file_name in missing_files:
            print(f"  • {file_name}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("Hospital Management System - Desktop Application")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return 1
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Check application files
    if not check_application_files():
        print("\nPlease ensure all application files are in the same directory as launch.py")
        input("Press Enter to exit...")
        return 1
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"⚠️  Missing dependencies: {', '.join(missing)}")
        response = input("Would you like to install them automatically? (y/n): ")
        
        if response.lower() in ['y', 'yes']:
            if not install_missing_packages(missing):
                print("❌ Failed to install some dependencies.")
                print("You can install them manually using:")
                print("  pip install tkcalendar==1.6.1 matplotlib==3.7.2 pandas==2.0.3 Pillow==10.0.0")
                input("Press Enter to exit...")
                return 1
        else:
            print("❌ Cannot start application without required dependencies.")
            input("Press Enter to exit...")
            return 1
    
    print("✓ All dependencies satisfied")
    print("🚀 Starting Hospital Management System...")
    print("-" * 50)
    
    try:
        # Add current directory to Python path
        current_dir = str(Path(__file__).parent)
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import and run the main application
        from desktop_app import HospitalManagementApp
        
        app = HospitalManagementApp()
        app.run()
        
        return 0
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please check if all application files are present and dependencies are installed.")
        input("Press Enter to exit...")
        return 1
    except Exception as e:
        print(f"❌ Application Error: {e}")
        print("An unexpected error occurred while running the application.")
        print("Please check the error details above and try again.")
        input("Press Enter to exit...")
        return 1

if __name__ == "__main__":
    exit(main())