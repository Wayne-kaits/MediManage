---
description: Repository Information Overview
alwaysApply: true
---

# MediManage Information

## Summary
MediManage is a comprehensive Hospital Management System with both web and desktop interfaces. It provides functionality for patient management, appointment scheduling, billing, lab test management, and reporting.

## Structure
- **root**: Main web application (Flask)
- **WindowsDesktopApp**: Standalone Windows desktop application
- **templates**: HTML templates for web interface
- **static**: CSS, JavaScript, and image assets
- **data**: Database storage location

## Projects

### Web Application (Flask)

#### Language & Runtime
**Language**: Python
**Version**: >=3.11
**Framework**: Flask 3.1.1
**Database**: SQLAlchemy with SQLite/PostgreSQL support

#### Dependencies
**Main Dependencies**:
- flask>=3.1.1
- flask-sqlalchemy>=3.1.1
- sqlalchemy>=2.0.41
- email-validator>=2.2.0
- psycopg2-binary>=2.9.10
- werkzeug>=3.1.3
- gunicorn>=23.0.0

#### Build & Installation
```bash
pip install -r requirements.txt
python main.py
```

#### Main Files
**Entry Point**: main.py
**Application**: app.py
**Database**: db.py
**Models**: models.py
**Routes**: routes.py
**Forms**: forms.py

### Windows Desktop Application

#### Language & Runtime
**Language**: Python
**Framework**: Tkinter (GUI)
**Database**: SQLite (shared with web app)

#### Dependencies
**Main Dependencies**:
- tkcalendar==1.6.1
- matplotlib==3.7.2
- pandas==2.0.3
- Pillow==10.0.0
- tkinter (built-in)
- sqlite3 (built-in)

#### Build & Installation
```bash
cd WindowsDesktopApp
pip install -r requirements.txt
python desktop_app.py
```

#### Build & Packaging
```bash
cd WindowsDesktopApp
python build_installer.py
```

#### Main Files
**Entry Point**: desktop_app.py
**Patient Management**: patient_management.py
**Appointment Management**: appointment_management.py
**Billing Management**: billing_management.py
**Lab Management**: lab_management.py
**Reports Management**: reports_management.py