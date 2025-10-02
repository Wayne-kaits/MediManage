"""
Routes update for MediManage with enhanced security, analytics, and performance
"""

# Add these imports to the top of routes.py
from flask import render_template, request, redirect, url_for, flash, session, jsonify, g, abort, send_file
from datetime import datetime, timedelta
from app import app, db
from models import User, Patient, Appointment, Bill, BillItem, LabTest
from forms import (validate_user_form, validate_patient_form, validate_appointment_form, 
                  validate_bill_form, validate_lab_test_form)
from utils import (generate_patient_id, generate_bill_number, generate_test_id, 
                  calculate_age, format_currency, get_appointment_status_badge,
                  get_bill_status_badge, get_lab_status_badge)
from security import (login_required, role_required, admin_required, log_audit, log_patient_access,
                     validate_password_strength, protect_against_csrf, validate_csrf_token,
                     refresh_session, sanitize_input, AuditLog, PatientAccessLog)
from analytics import Analytics
from cache import (cache, role_based_cache, user_based_cache, invalidate_patient_cache,
                  invalidate_appointment_cache, invalidate_bill_cache, invalidate_lab_cache,
                  invalidate_user_cache, QueryOptimizer)
import time
import json
import csv
import io
import os

# Initialize security on app startup
@app.before_first_request
def initialize_security():
    """Initialize security components"""
    with app.app_context():
        # Ensure audit log tables exist
        db.create_all()

@app.before_request
def load_logged_in_user():
    """Load user object on each request if logged in"""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
        
        # Check for session timeout (30 minutes of inactivity)
        if 'last_activity' in session:
            inactive_time = time.time() - session['last_activity']
            if inactive_time > 1800:  # 30 minutes
                session.clear()
                flash('Your session has expired due to inactivity', 'warning')
                return redirect(url_for('login'))
        
        session['last_activity'] = time.time()

@app.context_processor
def inject_csrf_token():
    """Inject CSRF token into all templates"""
    return dict(csrf_token=protect_against_csrf())

@app.context_processor
def inject_current_user():
    """Inject current user into all templates"""
    return dict(current_user=g.user if hasattr(g, 'user') else None)

@app.context_processor
def inject_datetime():
    """Inject datetime objects into all templates"""
    return dict(now=datetime.now(), timedelta=timedelta)

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        # Check if account is locked
        if user and user.account_locked_until and user.account_locked_until > datetime.utcnow():
            remaining_time = (user.account_locked_until - datetime.utcnow()).total_seconds() / 60
            flash(f'Account is locked. Please try again in {int(remaining_time)} minutes.', 'danger')
            log_audit(None, 'login_attempt_locked', 'user', user.id, 
                     f"Login attempt on locked account from {request.remote_addr}")
            return render_template('login.html')
        
        # Check credentials
        if user and user.check_password(password) and user.is_active:
            # Reset failed login attempts
            if hasattr(user, 'failed_login_attempts') and user.failed_login_attempts > 0:
                user.failed_login_attempts = 0
                user.account_locked_until = None
                db.session.commit()
            
            # Complete login
            session.clear()  # Prevent session fixation
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['last_activity'] = time.time()
            
            # Update last login time
            if hasattr(user, 'last_login'):
                user.last_login = datetime.utcnow()
                db.session.commit()
            
            log_audit(user.id, 'login_success', 'user', user.id, 
                     f"Successful login from {request.remote_addr}")
            
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Increment failed login attempts
            if user and hasattr(user, 'failed_login_attempts'):
                user.failed_login_attempts = getattr(user, 'failed_login_attempts', 0) + 1
                
                # Lock account after too many failed attempts
                if user.failed_login_attempts >= 5:
                    user.account_locked_until = datetime.utcnow() + timedelta(minutes=30)
                    log_audit(None, 'account_locked', 'user', user.id, 
                             f"Account locked after {user.failed_login_attempts} failed attempts from {request.remote_addr}")
                    flash('Too many failed login attempts. Account locked for 30 minutes.', 'danger')
                else:
                    log_audit(None, 'login_failed', 'user', user.id, 
                             f"Failed login attempt ({user.failed_login_attempts}) from {request.remote_addr}")
                    flash('Invalid username or password.', 'danger')
                
                db.session.commit()
            else:
                log_audit(None, 'login_invalid_user', 'auth', None, 
                         f"Login attempt with invalid username '{username}' from {request.remote_addr}")
                flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        log_audit(user_id, 'logout', 'user', user_id, f"User logged out from {request.remote_addr}")
    
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    user = g.user
    
    if request.method == 'POST':
        if not validate_csrf_token(request.form.get('csrf_token')):
            flash('Invalid form submission. Please try again.', 'danger')
            return redirect(url_for('change_password'))
            
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
        elif new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
        else:
            # Validate password strength
            is_valid, error_msg = validate_password_strength(new_password)
            if not is_valid:
                flash(error_msg, 'danger')
            else:
                user.set_password(new_password)
                if hasattr(user, 'require_password_change'):
                    user.require_password_change = False
                if hasattr(user, 'password_changed_at'):
                    user.password_changed_at = datetime.utcnow()
                db.session.commit()
                
                log_audit(user.id, 'password_changed', 'user', user.id, 
                         f"Password changed from {request.remote_addr}")
                
                # Refresh session after password change
                refresh_session()
                
                flash('Your password has been changed.', 'success')
                return redirect(url_for('dashboard'))
    
    return render_template('change_password.html', 
                         require_change=getattr(user, 'require_password_change', False))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management"""
    user = g.user
    
    if request.method == 'POST':
        if not validate_csrf_token(request.form.get('csrf_token')):
            flash('Invalid form submission. Please try again.', 'danger')
            return redirect(url_for('profile'))
            
        # Update profile information
        first_name = sanitize_input(request.form.get('first_name'))
        last_name = sanitize_input(request.form.get('last_name'))
        email = sanitize_input(request.form.get('email'))
        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        db.session.commit()
        
        # Invalidate user cache
        invalidate_user_cache(user.id)
        
        log_audit(user.id, 'profile_updated', 'user', user.id, 
                 f"Profile information updated from {request.remote_addr}")
        
        flash('Your profile has been updated.', 'success')
    
    # Get audit logs for this user
    audit_logs = AuditLog.query.filter_by(user_id=user.id).order_by(AuditLog.timestamp.desc()).limit(10).all()
    
    return render_template('profile.html', user=user, audit_logs=audit_logs)

# Patient routes with enhanced security and caching
@app.route('/patients')
@login_required
@role_based_cache(ttl=60)  # Cache for 1 minute based on user role
def patients_list():
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    
    query = Patient.query
    
    # Apply search filter
    if search:
        search = f"%{search}%"
        query = query.filter(
            db.or_(
                Patient.first_name.ilike(search),
                Patient.last_name.ilike(search),
                Patient.patient_id.ilike(search),
                Patient.phone.ilike(search),
                Patient.email.ilike(search)
            )
        )
    
    # Optimize query
    query = QueryOptimizer.optimize_patient_query(query)
    
    # Paginate results
    patients = QueryOptimizer.paginate_query(query.order_by(Patient.created_at.desc()), page)
    
    return render_template('patients/list.html', patients=patients, search=search)

@app.route('/patients/<int:patient_id>')
@login_required
@user_based_cache(ttl=60)  # Cache for 1 minute based on user ID
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Log patient access
    log_patient_access(g.user.id, patient_id, 'view', f"Viewed patient record from {request.remote_addr}")
    
    # Optimized queries with joins
    appointments = Appointment.query.filter_by(patient_id=patient_id).order_by(Appointment.appointment_date.desc()).all()
    bills = Bill.query.filter_by(patient_id=patient_id).order_by(Bill.created_at.desc()).all()
    lab_tests = LabTest.query.filter_by(patient_id=patient_id).order_by(LabTest.ordered_date.desc()).all()
    
    return render_template('patients/view.html', patient=patient, 
                         appointments=appointments, bills=bills, lab_tests=lab_tests)

@app.route('/patients/<int:patient_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    if request.method == 'POST':
        if not validate_csrf_token(request.form.get('csrf_token')):
            flash('Invalid form submission. Please try again.', 'danger')
            return redirect(url_for('edit_patient', patient_id=patient_id))
            
        validator = validate_patient_form(request.form)
        
        if validator.is_valid():
            # Sanitize input
            patient.first_name = sanitize_input(request.form['first_name'])
            patient.last_name = sanitize_input(request.form['last_name'])
            patient.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d')
            patient.gender = sanitize_input(request.form['gender'])
            patient.phone = sanitize_input(request.form['phone'])
            patient.email = sanitize_input(request.form['email'])
            patient.address = sanitize_input(request.form['address'])
            patient.emergency_contact = sanitize_input(request.form['emergency_contact'])
            patient.emergency_phone = sanitize_input(request.form['emergency_phone'])
            patient.blood_type = sanitize_input(request.form['blood_type'])
            patient.allergies = sanitize_input(request.form['allergies'])
            patient.medical_history = sanitize_input(request.form['medical_history'])
            
            db.session.commit()
            
            # Invalidate patient cache
            invalidate_patient_cache(patient_id)
            
            # Log patient access
            log_patient_access(g.user.id, patient_id, 'edit', f"Edited patient record from {request.remote_addr}")
            
            flash('Patient information updated successfully!', 'success')
            return redirect(url_for('view_patient', patient_id=patient.id))
        else:
            for field, errors in validator.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'danger')
    
    return render_template('patients/edit.html', patient=patient)

# Analytics routes
@app.route('/analytics')
@login_required
@role_required(['admin', 'doctor'])
@role_based_cache(ttl=300)  # Cache for 5 minutes based on user role
def analytics_dashboard():
    """Advanced analytics dashboard"""
    # Get analytics data
    dashboard_summary = Analytics.get_dashboard_summary()
    patient_demographics = Analytics.get_patient_demographics()
    appointment_trends = Analytics.get_appointment_trends(days=30)
    revenue_analytics = Analytics.get_revenue_analytics(months=12)
    lab_test_analytics = Analytics.get_lab_test_analytics()
    financial_insights = Analytics.get_financial_insights()
    operational_insights = Analytics.get_operational_insights()
    
    # Get doctor performance if user has admin role
    doctor_performance = None
    if g.user.role == 'admin':
        doctor_performance = Analytics.get_doctor_performance()
    
    # Get predictions if user has appropriate role
    predictions = None
    if g.user.role in ['admin', 'doctor']:
        predictions = {
            'appointment_load': Analytics.predict_appointment_load(days_ahead=7),
            'visit_frequency': Analytics.get_patient_visit_frequency()
        }
    
    # Log analytics access
    log_audit(g.user.id, 'analytics_viewed', 'analytics', None, 
             f"Analytics dashboard accessed from {request.remote_addr}")
    
    return render_template('analytics/dashboard.html',
                         dashboard_summary=dashboard_summary,
                         patient_demographics=patient_demographics,
                         appointment_trends=appointment_trends,
                         revenue_analytics=revenue_analytics,
                         lab_test_analytics=lab_test_analytics,
                         financial_insights=financial_insights,
                         operational_insights=operational_insights,
                         doctor_performance=doctor_performance,
                         predictions=predictions)

@app.route('/export-analytics', methods=['POST'])
@login_required
@role_required(['admin'])
def export_analytics_data():
    """Export analytics data for external analysis"""
    if not validate_csrf_token(request.form.get('csrf_token')):
        flash('Invalid form submission. Please try again.', 'danger')
        return redirect(url_for('analytics_dashboard'))
        
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Get data
    data = Analytics.export_data_for_analysis(start_date, end_date)
    
    # Create CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write patient data
    writer.writerow(['PATIENT DATA'])
    writer.writerow(['ID', 'Age', 'Gender', 'Blood Type'])
    for patient in data['patients']:
        writer.writerow([
            patient['id'],
            patient['age'],
            patient['gender'],
            patient['blood_type']
        ])
    
    writer.writerow([])  # Empty row as separator
    
    # Write appointment data
    writer.writerow(['APPOINTMENT DATA'])
    writer.writerow(['ID', 'Patient ID', 'Doctor ID', 'Date', 'Time', 'Type', 'Status', 'Duration'])
    for appointment in data['appointments']:
        writer.writerow([
            appointment['id'],
            appointment['patient_id'],
            appointment['doctor_id'],
            appointment['date'],
            appointment['time'],
            appointment['type'],
            appointment['status'],
            appointment['duration']
        ])
    
    writer.writerow([])  # Empty row as separator
    
    # Write billing data
    writer.writerow(['BILLING DATA'])
    writer.writerow(['ID', 'Patient ID', 'Date', 'Total Amount', 'Paid Amount', 'Balance', 'Status', 'Payment Method'])
    for bill in data['billing']:
        writer.writerow([
            bill['id'],
            bill['patient_id'],
            bill['date'],
            bill['total_amount'],
            bill['paid_amount'],
            bill['balance'],
            bill['status'],
            bill['payment_method']
        ])
    
    writer.writerow([])  # Empty row as separator
    
    # Write lab data
    writer.writerow(['LAB TEST DATA'])
    writer.writerow(['ID', 'Patient ID', 'Ordered By', 'Date', 'Type', 'Status'])
    for test in data['lab_tests']:
        writer.writerow([
            test['id'],
            test['patient_id'],
            test['ordered_by'],
            test['date'],
            test['type'],
            test['status']
        ])
    
    # Create response
    output.seek(0)
    
    # Log the export
    log_audit(g.user.id, 'analytics_export', 'analytics', None, 
             f"Analytics data exported from {request.remote_addr}")
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        attachment_filename=f'medimanage_analytics_{datetime.now().strftime("%Y%m%d")}.csv'
    )

# Security and audit routes
@app.route('/audit-logs')
@login_required
@admin_required
def view_audit_logs():
    """View system audit logs"""
    page = request.args.get('page', 1, type=int)
    user_filter = request.args.get('user_id')
    action_filter = request.args.get('action')
    resource_filter = request.args.get('resource_type')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = AuditLog.query
    
    # Apply filters
    if user_filter:
        query = query.filter(AuditLog.user_id == user_filter)
    if action_filter:
        query = query.filter(AuditLog.action == action_filter)
    if resource_filter:
        query = query.filter(AuditLog.resource_type == resource_filter)
    if date_from:
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(AuditLog.timestamp >= date_from)
    if date_to:
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        query = query.filter(AuditLog.timestamp <= date_to + timedelta(days=1))
    
    # Get logs with pagination
    logs = query.order_by(AuditLog.timestamp.desc()).paginate(page=page, per_page=50)
    
    # Get filter options
    users = User.query.all()
    actions = db.session.query(AuditLog.action).distinct().all()
    resource_types = db.session.query(AuditLog.resource_type).distinct().all()
    
    return render_template('security/audit_logs.html', 
                         logs=logs,
                         users=users,
                         actions=[a[0] for a in actions],
                         resource_types=[r[0] for r in resource_types],
                         user_filter=user_filter,
                         action_filter=action_filter,
                         resource_filter=resource_filter,
                         date_from=date_from,
                         date_to=date_to)

@app.route('/patient-access-logs')
@login_required
@admin_required
def view_patient_access_logs():
    """View patient access logs"""
    page = request.args.get('page', 1, type=int)
    user_filter = request.args.get('user_id')
    patient_filter = request.args.get('patient_id')
    action_filter = request.args.get('action')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = PatientAccessLog.query
    
    # Apply filters
    if user_filter:
        query = query.filter(PatientAccessLog.user_id == user_filter)
    if patient_filter:
        query = query.filter(PatientAccessLog.patient_id == patient_filter)
    if action_filter:
        query = query.filter(PatientAccessLog.action == action_filter)
    if date_from:
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(PatientAccessLog.timestamp >= date_from)
    if date_to:
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        query = query.filter(PatientAccessLog.timestamp <= date_to + timedelta(days=1))
    
    # Get logs with pagination and joins
    logs = query.join(User).join(Patient).order_by(PatientAccessLog.timestamp.desc()).paginate(page=page, per_page=50)
    
    # Get filter options
    users = User.query.all()
    patients = Patient.query.all()
    actions = db.session.query(PatientAccessLog.action).distinct().all()
    
    return render_template('security/patient_access_logs.html', 
                         logs=logs,
                         users=users,
                         patients=patients,
                         actions=[a[0] for a in actions],
                         user_filter=user_filter,
                         patient_filter=patient_filter,
                         action_filter=action_filter,
                         date_from=date_from,
                         date_to=date_to)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500