import random
import string
from datetime import datetime, timedelta

def generate_patient_id():
    """Generate a unique patient ID"""
    prefix = "P"
    timestamp = datetime.now().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{timestamp}{random_suffix}"

def generate_bill_number():
    """Generate a unique bill number"""
    prefix = "B"
    timestamp = datetime.now().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{timestamp}{random_suffix}"

def generate_test_id():
    """Generate a unique test ID"""
    prefix = "T"
    timestamp = datetime.now().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{timestamp}{random_suffix}"

def calculate_age(birth_date):
    """Calculate age from birth date"""
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    
    today = datetime.now().date()
    age = today.year - birth_date.year
    
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    
    return age

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"

def get_appointment_status_badge(status):
    """Get Bootstrap badge class for appointment status"""
    status_map = {
        'scheduled': 'bg-primary',
        'completed': 'bg-success',
        'cancelled': 'bg-danger'
    }
    return status_map.get(status, 'bg-secondary')

def get_bill_status_badge(status):
    """Get Bootstrap badge class for bill status"""
    status_map = {
        'pending': 'bg-warning text-dark',
        'paid': 'bg-success',
        'partial': 'bg-info',
        'overdue': 'bg-danger'
    }
    return status_map.get(status, 'bg-secondary')

def get_lab_status_badge(status):
    """Get Bootstrap badge class for lab test status"""
    status_map = {
        'ordered': 'bg-warning text-dark',
        'in_progress': 'bg-info',
        'completed': 'bg-success'
    }
    return status_map.get(status, 'bg-secondary')
