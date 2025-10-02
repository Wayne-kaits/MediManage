"""
Hospital Management System - EXE Installer Builder
Publisher: Kaitsnet IT Solutions
Creates a professional Windows executable installer
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
import zipfile
import tempfile

class InstallerBuilder:
    """Build professional Windows executable installer"""
    
    def __init__(self):
        self.app_name = "Hospital Management System"
        self.app_version = "1.0.0"
        self.publisher = "Kaitsnet IT Solutions"
        self.build_dir = Path(__file__).parent / "build"
        self.dist_dir = Path(__file__).parent / "dist"
        self.installer_name = f"HospitalManagementSystem_v{self.app_version}_Setup.exe"
        
        # Files to include in installer
        self.app_files = [
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
            "version_info.py",
            "installer_config.json"
        ]
        
        # Create directories
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
    
    def check_dependencies(self):
        """Check if required tools are installed"""
        print("Checking build dependencies...")
        
        required_tools = {
            "pyinstaller": "pip install pyinstaller",
            "nsis": "Download from https://nsis.sourceforge.io/"
        }
        
        missing_tools = []
        
        # Check PyInstaller
        try:
            import PyInstaller
            print("✓ PyInstaller found")
        except ImportError:
            missing_tools.append("pyinstaller")
            print("✗ PyInstaller not found")
        
        # Check NSIS (optional but recommended)
        nsis_paths = [
            r"C:\Program Files (x86)\NSIS\makensis.exe",
            r"C:\Program Files\NSIS\makensis.exe"
        ]
        
        nsis_found = any(os.path.exists(path) for path in nsis_paths)
        if nsis_found:
            print("✓ NSIS found")
        else:
            print("! NSIS not found (optional - for advanced installer)")
        
        if missing_tools:
            print("\nMissing dependencies:")
            for tool in missing_tools:
                print(f"  Install {tool}: {required_tools[tool]}")
            return False
        
        return True
    
    def create_spec_file(self):
        """Create PyInstaller spec file"""
        print("Creating PyInstaller spec file...")
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Application files
app_files = [
    ('desktop_app.py', '.'),
    ('patient_management.py', '.'),
    ('appointment_management.py', '.'),
    ('billing_management.py', '.'),
    ('lab_management.py', '.'),
    ('reports_management.py', '.'),
    ('user_management.py', '.'),
    ('launch.py', '.'),
    ('requirements.txt', '.'),
    ('README.md', '.'),
    ('version_info.py', '.'),
    ('installer_config.json', '.'),
]

# Hidden imports
hidden_imports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'tkinter.scrolledtext',
    'tkcalendar',
    'matplotlib',
    'matplotlib.backends.backend_tkagg',
    'pandas',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'sqlite3',
    'hashlib',
    'datetime',
    'pathlib',
    'json',
    'subprocess',
    'shutil',
    'winreg',
    'os',
    'sys',
    'threading',
    'webbrowser',
    'zipfile',
    'tempfile'
]

a = Analysis(
    ['setup.py'],
    pathex=[],
    binaries=[],
    datas=app_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.installer_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
        
        spec_file = self.build_dir / "installer.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        
        print(f"✓ Spec file created: {spec_file}")
        return spec_file
    
    def create_version_file(self):
        """Create version info file"""
        print("Creating version info file...")
        
        version_content = f'''# UTF-8
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
        [StringStruct(u'CompanyName', u'{self.publisher}'),
        StringStruct(u'FileDescription', u'{self.app_name} Setup Installer'),
        StringStruct(u'FileVersion', u'{self.app_version}'),
        StringStruct(u'InternalName', u'setup'),
        StringStruct(u'LegalCopyright', u'© 2024 {self.publisher}. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'{self.installer_name}'),
        StringStruct(u'ProductName', u'{self.app_name}'),
        StringStruct(u'ProductVersion', u'{self.app_version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
        
        version_file = self.build_dir / "version_info.txt"
        with open(version_file, 'w') as f:
            f.write(version_content)
        
        print(f"✓ Version file created: {version_file}")
        return version_file
    
    def create_app_icon(self):
        """Create a simple app icon if none exists"""
        print("Creating application icon...")
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a simple icon
            icon_size = 256
            icon = Image.new('RGBA', (icon_size, icon_size), (0, 123, 255, 255))
            draw = ImageDraw.Draw(icon)
            
            # Draw a simple medical cross
            cross_width = icon_size // 4
            cross_height = icon_size // 2
            x1 = (icon_size - cross_width) // 2
            y1 = (icon_size - cross_height) // 2
            x2 = x1 + cross_width
            y2 = y1 + cross_height
            
            # Vertical line
            draw.rectangle([x1, y1, x2, y2], fill='white')
            
            # Horizontal line
            h_x1 = (icon_size - cross_height) // 2
            h_y1 = (icon_size - cross_width) // 2
            h_x2 = h_x1 + cross_height
            h_y2 = h_y1 + cross_width
            draw.rectangle([h_x1, h_y1, h_x2, h_y2], fill='white')
            
            # Save as ICO
            icon_path = self.build_dir / "app_icon.ico"
            icon.save(icon_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
            
            print(f"✓ Icon created: {icon_path}")
            return icon_path
            
        except ImportError:
            print("! Pillow not available, skipping icon creation")
            return None
        except Exception as e:
            print(f"! Icon creation failed: {e}")
            return None
    
    def build_executable(self):
        """Build the executable using PyInstaller"""
        print("Building executable with PyInstaller...")
        
        spec_file = self.create_spec_file()
        version_file = self.create_version_file()
        icon_file = self.create_app_icon()
        
        # Build command - when using spec file, we only need the spec file path
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            str(spec_file)
        ]
        
        try:
            print("Running PyInstaller...")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.build_dir)
            
            if result.returncode == 0:
                print("✓ PyInstaller build successful")
                
                # Move executable to dist directory
                exe_path = self.build_dir / "dist" / self.installer_name
                if exe_path.exists():
                    final_path = self.dist_dir / self.installer_name
                    shutil.move(str(exe_path), str(final_path))
                    print(f"✓ Installer created: {final_path}")
                    return True
                else:
                    print("✗ Executable not found in build output")
                    return False
            else:
                print(f"✗ PyInstaller build failed:")
                print(result.stdout)
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"✗ Build process failed: {e}")
            return False
    
    def create_nsis_installer(self):
        """Create NSIS installer (optional)"""
        print("Creating NSIS installer...")
        
        nsis_script = f'''# Hospital Management System NSIS Installer
# Generated by build_installer.py

!define APP_NAME "{self.app_name}"
!define APP_VERSION "{self.app_version}"
!define APP_PUBLISHER "{self.publisher}"
!define APP_EXE "{self.installer_name}"

!include "MUI2.nsh"

Name "${{APP_NAME}}"
OutFile "{self.installer_name}"
InstallDir "$PROGRAMFILES\\${{APP_NAME}}"
InstallDirRegKey HKCU "Software\\${{APP_NAME}}" ""

!define MUI_ABORTWARNING
!define MUI_ICON "${{NSISDIR}}\\Contrib\\Graphics\\Icons\\modern-install.ico"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Section "MainApplication" SEC01
    SetOutPath "$INSTDIR"
    File "{self.installer_name}"
    
    CreateDirectory "$SMPROGRAMS\\${{APP_NAME}}"
    CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}"
    CreateShortCut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}"
    
    WriteUninstaller "$INSTDIR\\uninstall.exe"
    WriteRegStr HKCU "Software\\${{APP_NAME}}" "" $INSTDIR
    WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "DisplayName" "${{APP_NAME}}"
    WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "UninstallString" "$INSTDIR\\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\${{APP_EXE}}"
    Delete "$INSTDIR\\uninstall.exe"
    RMDir "$INSTDIR"
    
    Delete "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk"
    RMDir "$SMPROGRAMS\\${{APP_NAME}}"
    Delete "$DESKTOP\\${{APP_NAME}}.lnk"
    
    DeleteRegKey HKCU "Software\\${{APP_NAME}}"
    DeleteRegKey HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}"
SectionEnd'''
        
        nsis_file = self.build_dir / "installer.nsi"
        with open(nsis_file, 'w') as f:
            f.write(nsis_script)
        
        # Check if NSIS is available
        nsis_paths = [
            r"C:\Program Files (x86)\NSIS\makensis.exe",
            r"C:\Program Files\NSIS\makensis.exe"
        ]
        
        nsis_exe = None
        for path in nsis_paths:
            if os.path.exists(path):
                nsis_exe = path
                break
        
        if nsis_exe:
            try:
                result = subprocess.run([nsis_exe, str(nsis_file)], capture_output=True, text=True, cwd=self.build_dir)
                if result.returncode == 0:
                    print("✓ NSIS installer created")
                    return True
                else:
                    print("✗ NSIS installer creation failed")
                    return False
            except Exception as e:
                print(f"✗ NSIS error: {e}")
                return False
        else:
            print("! NSIS not found, skipping NSIS installer")
            return False
    
    def create_license_file(self):
        """Create license file"""
        print("Creating license file...")
        
        license_content = f'''{self.app_name} - License Agreement

Copyright (c) 2024 {self.publisher}

This software is provided "as is" without warranty of any kind.

By installing this software, you agree to the following terms:

1. This software is for use in healthcare facilities only
2. You are responsible for data security and HIPAA compliance
3. The software may not be redistributed without permission
4. Technical support is available through {self.publisher}

For support, contact: support@kaitsnet.com

All rights reserved.
'''
        
        license_file = self.build_dir / "LICENSE.txt"
        with open(license_file, 'w') as f:
            f.write(license_content)
        
        print(f"✓ License file created: {license_file}")
        return license_file
    
    def create_readme_installer(self):
        """Create README for installer"""
        print("Creating installer README...")
        
        readme_content = f'''{self.app_name} - Installation Guide
=====================================

Version: {self.app_version}
Publisher: {self.publisher}

INSTALLATION INSTRUCTIONS
-------------------------

1. Run the installer executable: {self.installer_name}
2. Follow the setup wizard
3. Choose installation directory
4. Complete installation
5. Launch from Start Menu or Desktop shortcut

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

SUPPORT
-------

For technical support:
- Email: support@kaitsnet.com
- Website: https://www.kaitsnet.com/support

LICENSE
-------

This software is licensed for use in healthcare facilities.
See LICENSE.txt for full terms.

© 2024 {self.publisher}. All rights reserved.
'''
        
        readme_file = self.dist_dir / "README_INSTALLER.txt"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        print(f"✓ README created: {readme_file}")
        return readme_file
    
    def build_installer(self):
        """Main build process"""
        print(f"Building {self.app_name} Installer")
        print("=" * 50)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Create license file
        self.create_license_file()
        
        # Build executable
        if not self.build_executable():
            return False
        
        # Try to create NSIS installer (optional)
        self.create_nsis_installer()
        
        # Create README
        self.create_readme_installer()
        
        print("\n" + "=" * 50)
        print("Build completed successfully!")
        print(f"Installer location: {self.dist_dir / self.installer_name}")
        print("=" * 50)
        
        return True

def main():
    """Main function"""
    builder = InstallerBuilder()
    success = builder.build_installer()
    
    if success:
        print("\n✓ Build process completed successfully!")
        return 0
    else:
        print("\n✗ Build process failed!")
        return 1

if __name__ == "__main__":
    exit(main())