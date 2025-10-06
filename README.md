# MediManage - Hospital Management System

A comprehensive web-based Hospital Management System built with Flask. Manage patients, appointments, billing, and lab tests efficiently with a modern, user-friendly interface.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Core Functionality
- **Patient Management** - Complete patient records with personal and medical information
- **Appointment Scheduling** - Book, manage, and track patient appointments
- **Billing System** - Create invoices, track payments, and manage billing records
- **Lab Test Management** - Order tests, record results, and track test status
- **User Management** - Role-based access control (Admin, Doctor, Nurse, Receptionist)

### User Interface
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI** - Clean, intuitive interface built with Bootstrap 5
- **Dashboard** - Quick overview of key metrics and recent activities
- **Search & Filter** - Easily find patients, appointments, and records

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/medimanage.git
cd medimanage
```

2. **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```

5. **Access the application**

Open your web browser and navigate to:
```
http://localhost:5000
```

### Default Login Credentials

After first run, you can register a new user or use default credentials if configured.

## 📁 Project Structure

```
MediManage/
├── app.py                  # Flask application setup
├── main.py                 # Application entry point
├── models.py               # Database models
├── routes.py               # Application routes
├── forms.py                # WTForms form definitions
├── db.py                   # Database configuration
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── dashboard.html     # Dashboard
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── patients/          # Patient templates
│   ├── appointments/      # Appointment templates
│   ├── billing/           # Billing templates
│   └── lab/               # Lab test templates
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── logo.png           # Application logo
└── data/                   # Database storage
    └── hospital.db        # SQLite database
```

## 🛠️ Technology Stack

- **Backend Framework:** Flask 3.1.1
- **Database:** SQLite (development) / PostgreSQL (production ready)
- **ORM:** SQLAlchemy 2.0.43
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Forms:** WTForms with validation
- **Authentication:** Flask session-based authentication
- **Password Security:** Werkzeug password hashing

## 📊 Database Schema

### Main Tables

- **Users** - System users with role-based access
- **Patients** - Patient records and medical information
- **Appointments** - Appointment scheduling and tracking
- **Bills** - Billing and payment records
- **LabTests** - Laboratory test orders and results

## 🔒 Security Features

- **Password Hashing** - Secure password storage using Werkzeug
- **Session Management** - Flask session-based authentication
- **Role-Based Access Control** - Different permissions for different user roles
- **SQL Injection Prevention** - SQLAlchemy ORM protection
- **CSRF Protection** - WTForms CSRF tokens

## 🎨 Customization

### Changing the Logo

Replace `static/logo.png` with your hospital's logo.

### Customizing Styles

Edit `static/css/style.css` to customize colors, fonts, and layout.

### Database Configuration

For production, configure PostgreSQL in `db.py`:

```python
# Change from SQLite to PostgreSQL
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/medimanage'
```

## 📝 Usage Guide

### Managing Patients

1. Navigate to **Patients** → **Add New Patient**
2. Fill in patient information
3. Save the record
4. View, edit, or delete patients from the patient list

### Scheduling Appointments

1. Go to **Appointments** → **New Appointment**
2. Select patient and doctor
3. Choose date and time
4. Add appointment notes
5. Save the appointment

### Creating Bills

1. Navigate to **Billing** → **New Bill**
2. Select patient
3. Add services and charges
4. Calculate total
5. Generate invoice

### Managing Lab Tests

1. Go to **Lab Tests** → **Add Lab Test**
2. Select patient
3. Choose test type
4. Submit order
5. Update results when available

## 🚢 Deployment

### Production Deployment

1. **Set environment variables**
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
```

2. **Use a production server**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

3. **Configure PostgreSQL**
- Update database URI in `db.py`
- Run migrations if needed

4. **Set up reverse proxy** (Nginx/Apache)
- Configure SSL certificates
- Set up domain name

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Bug Reports

If you discover any bugs, please create an issue on GitHub with:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🙏 Acknowledgments

- Flask framework and community
- Bootstrap for the UI components
- SQLAlchemy for database management
- All contributors and users

---

**Made with ❤️ for healthcare professionals**