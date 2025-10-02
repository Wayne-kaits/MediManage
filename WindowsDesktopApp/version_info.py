"""
Hospital Management System - Version Information
Publisher: Kaitsnet IT Solutions
"""

import sys
from datetime import datetime

# Application Information
APP_NAME = "Hospital Management System"
APP_VERSION = "1.0.1"
APP_BUILD = "2025.09.14.001"
APP_CODENAME = "Aesculapius"

# Publisher Information
PUBLISHER = "Kaitsnet IT Solutions"
PUBLISHER_WEBSITE = "https://www.kaitsnet.com"
PUBLISHER_EMAIL = "support@kaitsnet.com"
PUBLISHER_PHONE = "+1-555-KAITS-NET"

# Copyright Information
COPYRIGHT_YEAR = "2024"
COPYRIGHT_NOTICE = f"© {COPYRIGHT_YEAR} {PUBLISHER}. All rights reserved."

# License Information
LICENSE_TYPE = "Commercial"
LICENSE_VERSION = "1.0"
EULA_VERSION = "1.0"

# Build Information
BUILD_DATE = "2024-01-15"
BUILD_TIME = "14:30:00"
BUILD_TIMESTAMP = f"{BUILD_DATE} {BUILD_TIME}"
BUILD_ENVIRONMENT = "Production"
BUILD_CONFIGURATION = "Release"

# Version History
VERSION_HISTORY = [
    {
        "version": "1.0.0",
        "build": "2024.01.001",
        "date": "2024-01-15",
        "type": "Major Release",
        "changes": [
            "Initial release of MediManage",
            "Complete patient management system",
            "Advanced appointment scheduling",
            "Comprehensive billing system",
            "Lab test management with results",
            "Reports and analytics with charts",
            "User management with role-based access",
            "Modern dark theme UI",
            "Professional Windows installer"
        ]
    }
]

# System Requirements
MINIMUM_REQUIREMENTS = {
    "os": "Windows 10",
    "python": "3.7.0",
    "ram_mb": 4096,
    "disk_mb": 100,
    "resolution": "1366x768"
}

RECOMMENDED_REQUIREMENTS = {
    "os": "Windows 11",
    "python": "3.9.0",
    "ram_mb": 8192,
    "disk_mb": 500,
    "resolution": "1920x1080"
}

# Dependencies
DEPENDENCIES = {
    "tkcalendar": "1.6.1",
    "matplotlib": "3.7.2",
    "pandas": "2.0.3",
    "Pillow": "10.0.0"
}

# Features
FEATURES = [
    "Patient Management with Medical History",
    "Advanced Appointment Scheduling",
    "Comprehensive Billing System",
    "Lab Test Management with Results",
    "Reports & Analytics with Charts",
    "User Management with Role-based Access",
    "Modern Dark Theme Interface",
    "Data Export Capabilities",
    "Search and Filtering",
    "Real-time Data Validation",
    "Secure Authentication",
    "Database Integration",
    "Professional UI/UX"
]

# Support Information
SUPPORT_INFO = {
    "email": "support@kaitsnet.com",
    "website": "https://www.kaitsnet.com/support",
    "documentation": "https://kb.kaitsnet.com",
    "community": "https://community.kaitsnet.com",
    "phone": "+1-555-KAITS-NET",
    "hours": "Monday-Friday, 9 AM - 5 PM EST"
}

# Legal Information
LEGAL_INFO = {
    "privacy_policy": "https://www.kaitsnet.com/privacy",
    "terms_of_service": "https://www.kaitsnet.com/terms",
    "trademark": f"{APP_NAME} is a trademark of {PUBLISHER}",
    "patents": "Patent pending",
    "compliance": ["HIPAA Ready", "Data Protection Compliant"]
}


def get_version_string():
    """Get formatted version string"""
    return f"{APP_NAME} v{APP_VERSION} ({APP_BUILD})"


def get_full_version_info():
    """Get complete version information"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "build": APP_BUILD,
        "codename": APP_CODENAME,
        "publisher": PUBLISHER,
        "copyright": COPYRIGHT_NOTICE,
        "build_date": BUILD_DATE,
        "build_time": BUILD_TIME,
        "license": LICENSE_TYPE
    }


def get_system_info():
    """Get current system information"""
    import platform
    import os

    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "architecture": platform.architecture(),
        "processor": platform.processor(),
        "machine": platform.machine(),
        "node": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "user": os.environ.get("USERNAME", "Unknown"),
        "install_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def check_requirements():
    """Check if system meets minimum requirements"""
    import platform

    results = {
        "meets_requirements": True,
        "issues": []
    }

    # Check Python version
    python_version = sys.version_info
    min_python = tuple(map(int, MINIMUM_REQUIREMENTS["python"].split(".")))

    if python_version < min_python:
        results["meets_requirements"] = False
        results["issues"].append(f"Python {MINIMUM_REQUIREMENTS['python']} or higher required")

    # Check OS
    if platform.system() != "Windows":
        results["meets_requirements"] = False
        results["issues"].append("Windows operating system required")

    # Check Windows version
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
        winreg.CloseKey(key)

        if int(build_number) < 19041:  # Windows 10 build 2004
            results["issues"].append("Windows 10 version 2004 or higher recommended")
    except:
        pass

    return results


def print_version_info():
    """Print version information to console"""
    print("=" * 60)
    print(f"{APP_NAME}")
    print(f"Version: {APP_VERSION} (Build {APP_BUILD})")
    print(f"Codename: {APP_CODENAME}")
    print(f"Publisher: {PUBLISHER}")
    print(f"Build Date: {BUILD_TIMESTAMP}")
    print(f"License: {LICENSE_TYPE}")
    print(COPYRIGHT_NOTICE)
    print("=" * 60)

    # System requirements check
    req_check = check_requirements()
    if req_check["meets_requirements"]:
        print("✓ System meets minimum requirements")
    else:
        print("⚠ System requirements issues:")
        for issue in req_check["issues"]:
            print(f"  - {issue}")

    print("=" * 60)


def get_about_text():
    """Get formatted about text for UI"""
    return f"""{APP_NAME}
Version {APP_VERSION} (Build {APP_BUILD})
Codename: {APP_CODENAME}

{COPYRIGHT_NOTICE}

Publisher: {PUBLISHER}
Website: {PUBLISHER_WEBSITE}
Support: {PUBLISHER_EMAIL}

Build Information:
• Build Date: {BUILD_DATE}
• Build Environment: {BUILD_ENVIRONMENT}
• Configuration: {BUILD_CONFIGURATION}

License: {LICENSE_TYPE} License v{LICENSE_VERSION}

This software is designed for healthcare management and 
includes comprehensive features for patient care, 
appointment scheduling, billing, and reporting.

For support and documentation, visit:
{PUBLISHER_WEBSITE}/support"""


if __name__ == "__main__":
    print_version_info()

    # Print system information
    print("\nSystem Information:")
    sys_info = get_system_info()
    for key, value in sys_info.items():
        print(f"  {key}: {value}")

    print(f"\nDependencies:")
    for package, version in DEPENDENCIES.items():
        print(f"  {package}: {version}")

    print(f"\nFeatures ({len(FEATURES)}):")
    for i, feature in enumerate(FEATURES, 1):
        print(f"  {i:2d}. {feature}")