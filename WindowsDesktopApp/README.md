# Hospital Management System - Windows Desktop Application

A professional hospital management solution built with Python and Tkinter, featuring a modern dark theme interface.

## Features

- **Patient Management**: Complete patient records with medical history
- **Appointment Scheduling**: Advanced appointment booking and management
- **Billing System**: Comprehensive billing and payment tracking
- **Lab Test Management**: Lab test scheduling and results tracking
- **User Management**: Role-based access control
- **Reports & Analytics**: Charts and data visualization
- **Modern UI**: Bootstrap-inspired dark theme interface

## System Requirements

- Windows 10 or later
- Python 3.7 or higher
- 4GB RAM minimum
- 100MB free disk space
- 1366x768 minimum resolution

## Quick Start

### Option 1: Automatic Setup (Recommended)

1. **Download and Extract**: Extract all files to a folder
2. **Run Setup**: Double-click `setup.bat` to install dependencies
3. **Launch Application**: Double-click `run_app.bat` to start

### Option 2: Manual Setup

1. **Install Python**: Download Python 3.7+ from [python.org](https://www.python.org/downloads/)
2. **Install Dependencies**:
   ```bash
   pip install tkcalendar==1.6.1 matplotlib==3.7.2 pandas==2.0.3 Pillow==10.0.0
   ```
3. **Run Application**:
   ```bash
   python launch.py
   ```

## Default Login

- **Username**: `admin`
- **Password**: `admin123`

**Important**: Change the default password after first login!

## Building the Installer

To create a Windows executable installer:

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Run Build Script**:
   ```bash
   python build_installer.py
   ```
   
   Or use the batch file:
   ```bash
   build_exe.bat
   ```

3. **Find Installer**: The installer will be created in the `dist` folder

## Testing

Run the test suite to verify your setup:

```bash
python test_build.py
```

Or use the batch file:
```bash
run_tests.bat
```

## File Structure

```
WindowsDesktopApp/
├── desktop_app.py              # Main application
├── patient_management.py       # Patient management module
├── appointment_management.py   # Appointment management module
├── billing_management.py       # Billing management module
├── lab_management.py          # Lab test management module
├── reports_management.py      # Reports and analytics module
├── user_management.py         # User management module
├── launch.py                  # Application launcher
├── setup.py                   # Setup installer
├── build_installer.py         # Build script
├── test_build.py              # Test suite
├── requirements.txt           # Python dependencies
├── setup.bat                  # Setup batch file
├── run_app.bat                # Run application batch file
├── run_tests.bat              # Run tests batch file
├── build_exe.bat              # Build installer batch file
├── build_config.json          # Build configuration
├── installer_config.json      # Installer configuration
└── README.md                  # This file
```

## Troubleshooting

### Common Issues

1. **Python not found**: Install Python and add to PATH
2. **Missing dependencies**: Run `setup.bat` or install manually
3. **Import errors**: Ensure all files are in the same directory
4. **Build failures**: Check PyInstaller installation and dependencies

### Error Messages

- **"Python is not installed"**: Install Python 3.7+ from python.org
- **"Missing dependencies"**: Run `setup.bat` to install automatically
- **"Import Error"**: Check if all application files are present
- **"Build failed"**: Ensure PyInstaller is installed and try again

## Support

For technical support:
- **Email**: support@kaitsnet.com
- **Website**: https://www.kaitsnet.com/support
- **Documentation**: Check the BUILD_INSTRUCTIONS.md file

## License

This software is licensed for use in healthcare facilities.
See LICENSE.txt for complete terms and conditions.

© 2024 Kaitsnet IT Solutions. All rights reserved.

## Recent Fixes

- Fixed matplotlib import issues in test suite
- Improved error handling in launch script
- Enhanced build installer with better dependency management
- Added automatic icon creation for installer
- Improved setup process with better error messages
- Added comprehensive test suite
- Fixed path issues in various modules
- Enhanced PowerShell build script
- Added batch files for easy execution

## Version History

- **v1.0.0**: Initial release with all core features
- **v1.0.1**: Bug fixes and improved error handling
- **v1.0.2**: Enhanced build process and testing