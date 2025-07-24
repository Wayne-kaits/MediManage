# Hospital Management System

## Overview

This is a comprehensive Hospital Management System built with Flask and SQLAlchemy. The system provides functionality for managing patients, appointments, billing, lab tests, and user authentication with role-based access control. It features a modern web interface using Bootstrap with dark theme support.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a traditional Flask web application architecture with the following structure:

- **Backend Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite (default) with PostgreSQL support via environment configuration
- **Frontend**: Server-side rendered templates using Jinja2 with Bootstrap CSS framework
- **Authentication**: Session-based authentication with password hashing
- **Styling**: Bootstrap dark theme with Font Awesome icons

## Key Components

### 1. Application Core (`app.py`)
- Flask application initialization and configuration
- SQLAlchemy database setup with DeclarativeBase
- Environment-based configuration for database and secrets
- Proxy middleware support for deployment

### 2. Data Models (`models.py`)
- **User Model**: Staff authentication with role-based access (admin, doctor, staff)
- **Patient Model**: Complete patient information with medical history
- **Appointment Model**: (Referenced but not shown in files)
- **Bill & BillItem Models**: (Referenced but not shown in files)
- **LabTest Model**: (Referenced but not shown in files)

### 3. Form Validation (`forms.py`)
- Custom form validator class with chainable validation methods
- Supports required fields, email format, date/datetime validation, and numeric validation
- Error collection and reporting system

### 4. Utility Functions (`utils.py`)
- ID generation for patients, bills, and tests
- Age calculation from birth dates
- Currency formatting
- Status badge helpers for UI consistency

### 5. Routing System (`routes.py`)
- Authentication decorators for login and role-based access
- Context processors for template utilities
- Modular route organization by feature area

### 6. Template System
- Base template with responsive navigation
- Feature-specific template directories (patients, appointments, billing, lab, reports)
- Dark theme Bootstrap integration
- Print-friendly styling

## Data Flow

1. **User Authentication**: Session-based login with role verification
2. **Patient Management**: CRUD operations with unique patient ID generation
3. **Appointment Scheduling**: Links patients with doctors and time slots
4. **Billing System**: Associates costs with patients and appointments
5. **Lab Testing**: Order and track medical tests with results
6. **Reporting**: Analytics and data visualization

## External Dependencies

- **Flask**: Web framework and templating
- **SQLAlchemy**: Database ORM and migrations
- **Werkzeug**: Password hashing and WSGI utilities
- **Bootstrap**: Frontend CSS framework (CDN)
- **Font Awesome**: Icon library (CDN)

## Deployment Strategy

The application is configured for flexible deployment:

- **Development**: SQLite database with debug mode
- **Production**: PostgreSQL support via DATABASE_URL environment variable
- **Session Management**: Configurable secret key via SESSION_SECRET
- **Proxy Support**: ProxyFix middleware for reverse proxy deployments
- **Static Assets**: External CDN dependencies for Bootstrap and Font Awesome

The system uses environment variables for configuration, making it suitable for various hosting platforms including cloud services that provide database URLs and session secrets through environment configuration.