"""
Security utilities for MediManage
Includes authentication, authorization, and audit logging
"""

import os
import time
import hashlib
import secrets
from functools import wraps
from datetime import datetime, timedelta
from flask import request, session, redirect, url_for, flash, g, current_app, abort
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from db import db

# Constants
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 30  # minutes
PASSWORD_EXPIRY = 90  # days
SESSION_TIMEOUT = 30  # minutes
SENSITIVE_OPERATIONS = ['patient_edit', 'patient_delete', 'billing_create', 'billing_edit']

# Security settings
PASSWORD_MIN_LENGTH = 8
PASSWORD_COMPLEXITY = True  # Require mixed case, numbers, and special characters
ENABLE_BRUTE_FORCE_PROTECTION = True
ENABLE_SESSION_FIXATION_PROTECTION = True
ENABLE_AUDIT_LOGGING = True

class AuditLog(db.Model):
    """Audit log model for tracking security events"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    action = db.Column(db.String(50), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)
    resource_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    
    # Relationship
    user = db.relationship('User', backref='audit_logs')

class PatientAccessLog(db.Model):
    """Patient access log for tracking PHI access"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # view, edit, delete
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='patient_access_logs')
    patient = db.relationship('Patient', backref='access_logs')

def log_audit(user_id, action, resource_type, resource_id=None, details=None):
    """Log an audit entry"""
    if not ENABLE_AUDIT_LOGGING:
        return
        
    log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string if request.user_agent else None
    )
    db.session.add(log)
    db.session.commit()

def log_patient_access(user_id, patient_id, action, details=None):
    """Log patient data access"""
    if not ENABLE_AUDIT_LOGGING:
        return
        
    log = PatientAccessLog(
        user_id=user_id,
        patient_id=patient_id,
        action=action,
        details=details,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

def validate_password_strength(password):
    """Validate password strength"""
    if len(password) < PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"
    
    if PASSWORD_COMPLEXITY:
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        if not (has_upper and has_lower and has_digit and has_special):
            return False, "Password must include uppercase, lowercase, numbers, and special characters"
    
    return True, None

def generate_secure_token(length=32):
    """Generate a secure random token"""
    return secrets.token_hex(length)

def hash_data(data):
    """Create a secure hash of data"""
    return hashlib.sha256(str(data).encode()).hexdigest()

def login_required(f):
    """Decorator to require login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login', next=request.url))
        
        # Check if user exists and is active
        user = User.query.get(session['user_id'])
        if not user or not user.is_active:
            session.clear()
            flash('Your account is no longer active', 'danger')
            return redirect(url_for('login'))
        
        # Check for session timeout
        if 'last_activity' in session:
            inactive_time = time.time() - session['last_activity']
            if inactive_time > (SESSION_TIMEOUT * 60):  # Convert minutes to seconds
                session.clear()
                flash('Your session has expired due to inactivity', 'warning')
                return redirect(url_for('login'))
        
        # Update last activity time
        session['last_activity'] = time.time()
        
        # Set user in global context
        g.user = user
        
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    """Decorator to require specific role(s) for a route"""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not isinstance(roles, list):
                role_list = [roles]
            else:
                role_list = roles
                
            if g.user.role not in role_list:
                log_audit(g.user.id, 'role_denied', 'route', 
                         details=f"Attempted to access {request.path} requiring role(s) {role_list}")
                flash('You do not have the required role to access this resource', 'danger')
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator to require admin role for a route"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if g.user.role != 'admin':
            log_audit(g.user.id, 'admin_denied', 'route', 
                     details=f"Attempted to access admin route {request.path}")
            flash('Administrator access required', 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def protect_against_csrf():
    """Generate and validate CSRF tokens"""
    if 'csrf_token' not in session:
        session['csrf_token'] = generate_secure_token()
    return session['csrf_token']

def validate_csrf_token(form_token):
    """Validate a CSRF token from a form"""
    if 'csrf_token' not in session or session['csrf_token'] != form_token:
        return False
    return True

def refresh_session():
    """Refresh the session to prevent session fixation attacks"""
    if ENABLE_SESSION_FIXATION_PROTECTION:
        # Keep important session data
        user_id = session.get('user_id')
        username = session.get('username')
        role = session.get('role')
        
        # Clear the session
        session.clear()
        
        # Restore important data with a new session ID
        session['user_id'] = user_id
        session['username'] = username
        session['role'] = role
        session['last_activity'] = time.time()
        
        # Generate a new CSRF token
        session['csrf_token'] = generate_secure_token()

def sanitize_input(input_data):
    """Sanitize user input to prevent XSS and injection attacks"""
    if isinstance(input_data, str):
        # Basic sanitization - replace potentially dangerous characters
        sanitized = input_data.replace('<', '&lt;').replace('>', '&gt;')
        return sanitized
    elif isinstance(input_data, dict):
        return {k: sanitize_input(v) for k, v in input_data.items()}
    elif isinstance(input_data, list):
        return [sanitize_input(item) for item in input_data]
    else:
        return input_data