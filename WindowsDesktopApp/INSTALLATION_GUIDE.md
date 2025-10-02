# Hospital Management System - Installation Guide

**Publisher:** Kaitsnet IT Solutions  
**Version:** 1.0.0  
**Release Date:** January 2024

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-Installation Checklist](#pre-installation-checklist)
3. [Installation Methods](#installation-methods)
4. [Step-by-Step Installation](#step-by-step-installation)
5. [Post-Installation Setup](#post-installation-setup)
6. [Troubleshooting](#troubleshooting)
7. [Uninstallation](#uninstallation)
8. [Support](#support)

---

## 🖥️ System Requirements

### Minimum Requirements
- **Operating System:** Windows 10 (64-bit)
- **Python:** 3.7 or higher
- **RAM:** 4GB
- **Storage:** 100MB free disk space
- **Display:** 1366x768 resolution
- **Network:** Internet connection for initial setup

### Recommended Requirements
- **Operating System:** Windows 11 (64-bit)
- **Python:** 3.9 or higher
- **RAM:** 8GB or more
- **Storage:** 500MB free disk space
- **Display:** 1920x1080 resolution or higher
- **Network:** Broadband internet connection

### Required Software
- Python 3.7+ with tkinter support
- Windows PowerShell (for advanced features)
- Administrator privileges (recommended)

---

## ✅ Pre-Installation Checklist

Before installing the Hospital Management System, ensure you have:

- [ ] **Python Installed**: Download from [python.org](https://www.python.org/downloads/)
  - ⚠️ **Important**: Check "Add Python to PATH" during Python installation
- [ ] **Administrator Rights**: Right-click installer and select "Run as administrator"
- [ ] **Antivirus Disabled**: Temporarily disable antivirus during installation
- [ ] **Sufficient Disk Space**: At least 100MB free space
- [ ] **Stable Internet**: For downloading dependencies
- [ ] **Backup Existing Data**: If upgrading from previous version

### Python Installation Verification
Open Command Prompt and run:
```cmd
python --version
```
You should see output like: `Python 3.9.x`

---

## 🚀 Installation Methods

### Method 1: Professional Setup Wizard (Recommended)
1. Double-click `setup.bat`
2. Follow the guided installation wizard
3. Accept the End User License Agreement
4. Choose installation directory
5. Select installation options
6. Complete the installation

### Method 2: Manual Installation
1. Run `python setup.py` from command line
2. Follow the setup wizard steps
3. Configure installation options manually

### Method 3: Quick Launch
1. Run `python launch.py` for dependency checking
2. Automatically installs missing packages
3. Launches application directly

---

## 📖 Step-by-Step Installation

### Step 1: Welcome Screen
- Review system requirements
- Verify Python installation
- Click "Next" to continue

### Step 2: License Agreement
- **Read the End User License Agreement carefully**
- Key points to note:
  - Software is licensed, not sold
  - Healthcare compliance responsibilities
  - Data security requirements
  - Support and update policies
- Check "I accept the terms in the License Agreement"
- Click "Next" to proceed

### Step 3: Installation Directory
- **Default Location**: `C:\Program Files\Kaitsnet IT Solutions\Hospital Management System`
- **Custom Location**: Click "Browse" to select different folder
- **Space Requirements**: Verify sufficient disk space
- Click "Next" to continue

### Step 4: Installation Options
Configure the following options:

#### Shortcuts
- [x] **Create desktop shortcut** - Quick access from desktop
- [x] **Create Start Menu shortcut** - Access from Start Menu

#### Additional Options
- [ ] **Launch application after installation** - Auto-start after setup
- [x] **Register application in Windows Programs** - Add to Programs & Features

### Step 5: Installation Progress
- **Automatic Process**: Files are copied and configured
- **Dependency Installation**: Python packages are installed
- **Registry Updates**: Application is registered
- **Shortcut Creation**: Desktop and Start Menu shortcuts
- **Progress Monitoring**: Real-time installation log

### Step 6: Installation Complete
- **Success Confirmation**: Installation completed successfully
- **Default Credentials**: 
  - Username: `admin`
  - Password: `admin123`
- **Launch Option**: Start application immediately (if selected)

---

## ⚙️ Post-Installation Setup

### First Launch
1. **Start the Application**:
   - Desktop shortcut: Double-click "Hospital Management System"
   - Start Menu: Start → Kaitsnet IT Solutions → Hospital Management System
   - Command line: Navigate to install directory and run `python launch.py`

2. **Initial Login**:
   - Username: `admin`
   - Password: `admin123`

### Essential Configuration Steps

#### 1. Change Default Password
- Go to **User Management** (Admin only)
- Select admin user
- Click "Reset Password"
- Set a strong, secure password

#### 2. Create User Accounts
- Add doctors, staff, and other users
- Assign appropriate roles:
  - **Admin**: Full system access
  - **Doctor**: Patient care, appointments, lab tests
  - **Staff**: Data entry, scheduling, billing

#### 3. System Configuration
- Set up appointment types
- Configure lab test categories
- Customize billing items
- Set up report preferences

#### 4. Data Import (Optional)
- Import existing patient data
- Transfer appointment history
- Migrate billing records

### Security Recommendations
- Change default admin password immediately
- Create individual user accounts (avoid sharing)
- Regular database backups
- Keep software updated
- Use strong passwords
- Enable Windows Firewall

---

## 🔧 Troubleshooting

### Common Installation Issues

#### Python Not Found
**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
1. Install Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Restart Command Prompt
4. Verify with `python --version`

#### Permission Denied
**Error**: `Permission denied` or `Access is denied`

**Solution**:
1. Right-click installer
2. Select "Run as administrator"
3. Confirm UAC prompt
4. Retry installation

#### Dependency Installation Failed
**Error**: Package installation errors

**Solution**:
1. Check internet connection
2. Update pip: `python -m pip install --upgrade pip`
3. Install manually: `pip install tkcalendar matplotlib pandas Pillow`
4. Retry setup

#### Application Won't Start
**Error**: Application crashes on startup

**Solution**:
1. Check Python version: `python --version`
2. Verify dependencies: `pip list`
3. Check installation directory permissions
4. Review error logs in installation directory
5. Reinstall application

#### Database Errors
**Error**: Database connection or creation issues

**Solution**:
1. Check write permissions in installation directory
2. Ensure `data` folder exists
3. Delete `hospital.db` to reset (loses data)
4. Run as administrator

### Performance Issues

#### Slow Startup
- Close unnecessary applications
- Increase available RAM
- Check disk space
- Update graphics drivers

#### UI Display Problems
- Check screen resolution (minimum 1366x768)
- Adjust Windows display scaling
- Update graphics drivers
- Verify tkinter installation

---

## 🗑️ Uninstallation

### Method 1: Windows Programs & Features
1. Open **Settings** → **Apps**
2. Search for "Hospital Management System"
3. Click **Uninstall**
4. Follow uninstall wizard

### Method 2: Uninstaller Script
1. Navigate to installation directory
2. Run `uninstall.py`
3. Confirm uninstallation
4. Application and shortcuts are removed

### Manual Removal
If automatic uninstallation fails:

1. **Delete Installation Directory**:
   - Default: `C:\Program Files\Kaitsnet IT Solutions\Hospital Management System`

2. **Remove Shortcuts**:
   - Desktop: Delete "Hospital Management System.lnk"
   - Start Menu: Delete from Kaitsnet IT Solutions folder

3. **Registry Cleanup** (Advanced):
   - Open Registry Editor (regedit)
   - Navigate to: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall`
   - Delete "HospitalManagementSystem" key

4. **Data Backup**:
   - Save `hospital.db` if you want to keep data
   - Export reports and patient data

---

## 📞 Support

### Getting Help

#### Documentation
- **User Guide**: Built-in help system
- **README**: Installation directory
- **Online Documentation**: [kb.kaitsnet.com](https://kb.kaitsnet.com)

#### Technical Support
- **Email**: support@kaitsnet.com
- **Response Time**: 24-48 hours
- **Business Hours**: Monday-Friday, 9 AM - 5 PM EST

#### Community Support
- **Forum**: [community.kaitsnet.com](https://community.kaitsnet.com)
- **Knowledge Base**: [kb.kaitsnet.com](https://kb.kaitsnet.com)
- **Video Tutorials**: Available on website

### Before Contacting Support

Please have the following information ready:
- Application version
- Operating system version
- Python version
- Error messages (screenshots helpful)
- Steps to reproduce the issue
- Installation log files

### Support Scope

#### Included Support
- Installation assistance
- Basic configuration help
- Bug reports and fixes
- Feature questions
- Performance optimization

#### Additional Services
- Custom configuration
- Data migration assistance
- Training sessions
- Extended support contracts
- Custom development

---

## 📄 Legal Information

### License Agreement
By installing this software, you agree to the End User License Agreement (EULA) presented during installation.

### Healthcare Compliance
This software is designed for healthcare management. Users are responsible for:
- HIPAA compliance
- Local privacy regulations
- Medical record keeping requirements
- Data security measures
- Regular backups

### Disclaimer
Kaitsnet IT Solutions provides this software "as is" without warranty. Users are responsible for data backup and security.

### Copyright
© 2024 Kaitsnet IT Solutions. All rights reserved.

---

## 📋 Installation Checklist

Print this checklist and check off each step:

**Pre-Installation**
- [ ] Python 3.7+ installed with PATH
- [ ] Administrator privileges available
- [ ] Sufficient disk space (100MB+)
- [ ] Internet connection active
- [ ] Antivirus temporarily disabled

**Installation Process**
- [ ] Setup wizard launched successfully
- [ ] License agreement read and accepted
- [ ] Installation directory selected
- [ ] Installation options configured
- [ ] Dependencies installed successfully
- [ ] Shortcuts created
- [ ] Application registered

**Post-Installation**
- [ ] Application launches successfully
- [ ] Default login works (admin/admin123)
- [ ] Admin password changed
- [ ] User accounts created
- [ ] System configured for use
- [ ] Data backup plan established

**Verification**
- [ ] All modules accessible
- [ ] Patient management works
- [ ] Appointments can be scheduled
- [ ] Billing system functional
- [ ] Lab tests can be ordered
- [ ] Reports generate correctly
- [ ] User management accessible (admin)

---

**Installation Guide Version:** 1.0  
**Last Updated:** January 2024  
**Publisher:** Kaitsnet IT Solutions

For the most current version of this guide, visit: [www.kaitsnet.com/support](https://www.kaitsnet.com/support)