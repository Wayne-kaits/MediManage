from flask import render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime, timedelta
from app import app, db
from models import User, Patient, Appointment, Bill, BillItem, LabTest
from forms import (validate_user_form, validate_patient_form, validate_appointment_form, 
                  validate_bill_form, validate_lab_test_form)
from utils import (generate_patient_id, generate_bill_number, generate_test_id, 
                  calculate_age, format_currency, get_appointment_status_badge,
                  get_bill_status_badge, get_lab_status_badge)

# Authentication decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def role_required(roles):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            
            user = User.query.get(session['user_id'])
            if not user or user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

@app.context_processor
def utility_processor():
    return dict(
        calculate_age=calculate_age,
        format_currency=format_currency,
        get_appointment_status_badge=get_appointment_status_badge,
        get_bill_status_badge=get_bill_status_badge,
        get_lab_status_badge=get_lab_status_badge
    )

# Home route
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('POST to /login:', dict(request.form))  # DEBUG
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@role_required(['admin'])
def register():
    if request.method == 'POST':
        validator = validate_user_form(request.form)
        
        if validator.is_valid():
            # Check if username or email already exists
            existing_user = User.query.filter(
                (User.username == request.form['username']) | 
                (User.email == request.form['email'])
            ).first()
            
            if existing_user:
                flash('Username or email already exists.', 'danger')
            else:
                user = User()
                user.username = request.form['username']
                user.email = request.form['email']
                user.role = request.form['role']
                user.first_name = request.form['first_name']
                user.last_name = request.form['last_name']
                user.set_password(request.form['password'])
                
                db.session.add(user)
                db.session.commit()
                
                flash('User registered successfully!', 'success')
                return redirect(url_for('dashboard'))
        else:
            for field, error in validator.errors.items():
                flash(f'{field}: {error}', 'danger')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Get statistics for dashboard
    total_patients = Patient.query.count()
    today = datetime.now().date()
    today_appointments = Appointment.query.filter(
        db.func.date(Appointment.appointment_date) == today
    ).count()
    pending_bills = Bill.query.filter_by(status='pending').count()
    pending_tests = LabTest.query.filter_by(status='ordered').count()
    
    # Recent activities
    recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         total_patients=total_patients,
                         today_appointments=today_appointments,
                         pending_bills=pending_bills,
                         pending_tests=pending_tests,
                         recent_patients=recent_patients,
                         recent_appointments=recent_appointments)

# Patient routes
@app.route('/patients')
@login_required
def patients_list():
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    
    query = Patient.query
    if search:
        query = query.filter(
            (Patient.first_name.contains(search)) |
            (Patient.last_name.contains(search)) |
            (Patient.patient_id.contains(search)) |
            (Patient.phone.contains(search))
        )
    
    patients = query.order_by(Patient.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('patients/list.html', patients=patients, search=search)

@app.route('/patients/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        validator = validate_patient_form(request.form)
        
        if validator.is_valid():
            patient = Patient()
            patient.patient_id = generate_patient_id()
            patient.first_name = request.form['first_name']
            patient.last_name = request.form['last_name']
            patient.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            patient.gender = request.form['gender']
            patient.phone = request.form.get('phone')
            patient.email = request.form.get('email')
            patient.address = request.form.get('address')
            patient.emergency_contact = request.form.get('emergency_contact')
            patient.emergency_phone = request.form.get('emergency_phone')
            patient.blood_type = request.form.get('blood_type')
            patient.allergies = request.form.get('allergies')
            patient.medical_history = request.form.get('medical_history')
            
            db.session.add(patient)
            db.session.commit()
            
            flash('Patient added successfully!', 'success')
            return redirect(url_for('patients_list'))
        else:
            for field, error in validator.errors.items():
                flash(f'{field}: {error}', 'danger')
    
    return render_template('patients/add.html')

@app.route('/patients/<int:patient_id>')
@login_required
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
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
        validator = validate_patient_form(request.form)
        
        if validator.is_valid():
            patient.first_name = request.form['first_name']
            patient.last_name = request.form['last_name']
            patient.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            patient.gender = request.form['gender']
            patient.phone = request.form.get('phone')
            patient.email = request.form.get('email')
            patient.address = request.form.get('address')
            patient.emergency_contact = request.form.get('emergency_contact')
            patient.emergency_phone = request.form.get('emergency_phone')
            patient.blood_type = request.form.get('blood_type')
            patient.allergies = request.form.get('allergies')
            patient.medical_history = request.form.get('medical_history')
            patient.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            flash('Patient updated successfully!', 'success')
            return redirect(url_for('view_patient', patient_id=patient_id))
        else:
            for field, error in validator.errors.items():
                flash(f'{field}: {error}', 'danger')
    
    return render_template('patients/edit.html', patient=patient)

# Appointment routes
@app.route('/appointments')
@login_required
def appointments_list():
    date_filter = request.args.get('date')
    status_filter = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    
    query = Appointment.query
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Appointment.appointment_date) == filter_date)
        except ValueError:
            flash('Invalid date format', 'danger')
    
    if status_filter and status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    appointments = query.order_by(Appointment.appointment_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('appointments/list.html', appointments=appointments, 
                         date_filter=date_filter, status_filter=status_filter)

@app.route('/appointments/add', methods=['GET', 'POST'])
@login_required
def add_appointment():
    if request.method == 'POST':
        validator = validate_appointment_form(request.form)
        
        if validator.is_valid():
            appointment = Appointment()
            appointment.patient_id = request.form['patient_id']
            appointment.doctor_id = request.form['doctor_id']
            appointment.appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%dT%H:%M')
            appointment.appointment_type = request.form['appointment_type']
            appointment.notes = request.form.get('notes')
            
            db.session.add(appointment)
            db.session.commit()
            
            flash('Appointment scheduled successfully!', 'success')
            return redirect(url_for('appointments_list'))
        else:
            for field, error in validator.errors.items():
                flash(f'{field}: {error}', 'danger')
    
    patients = Patient.query.order_by(Patient.first_name).all()
    doctors = User.query.filter_by(role='doctor').order_by(User.first_name).all()
    
    return render_template('appointments/add.html', patients=patients, doctors=doctors)

@app.route('/appointments/<int:appointment_id>')
@login_required
def view_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template('appointments/view.html', appointment=appointment)

# Billing routes
@app.route('/billing')
@login_required
def billing_list():
    status_filter = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    
    query = Bill.query
    
    if status_filter and status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    bills = query.order_by(Bill.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('billing/list.html', bills=bills, status_filter=status_filter)

@app.route('/billing/add', methods=['GET', 'POST'])
@login_required
def add_bill():
    if request.method == 'POST':
        validator = validate_bill_form(request.form)
        
        if validator.is_valid():
            bill = Bill()
            bill.bill_number = generate_bill_number()
            bill.patient_id = request.form['patient_id']
            bill.appointment_id = request.form.get('appointment_id') or None
            bill.total_amount = float(request.form['total_amount'])
            bill.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
            bill.notes = request.form.get('notes')
            
            db.session.add(bill)
            db.session.flush()  # Get the bill ID
            
            # Add bill items if provided
            descriptions = request.form.getlist('item_description[]')
            quantities = request.form.getlist('item_quantity[]')
            unit_prices = request.form.getlist('item_unit_price[]')
            
            for i, desc in enumerate(descriptions):
                if desc.strip():
                    qty = int(quantities[i]) if quantities[i] else 1
                    price = float(unit_prices[i]) if unit_prices[i] else 0.0
                    
                    bill_item = BillItem()
                    bill_item.bill_id = bill.id
                    bill_item.description = desc
                    bill_item.quantity = qty
                    bill_item.unit_price = price
                    bill_item.total_price = qty * price
                    db.session.add(bill_item)
            
            db.session.commit()
            
            flash('Bill created successfully!', 'success')
            return redirect(url_for('billing_list'))
        else:
            for field, error in validator.errors.items():
                flash(f'{field}: {error}', 'danger')
    
    patients = Patient.query.order_by(Patient.first_name).all()
    appointments = Appointment.query.filter_by(status='completed').order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('billing/add.html', patients=patients, appointments=appointments)

@app.route('/billing/<int:bill_id>')
@login_required
def view_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    return render_template('billing/view.html', bill=bill)

# Lab routes
@app.route('/lab')
@login_required
def lab_list():
    status_filter = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    
    query = LabTest.query
    
    if status_filter and status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    lab_tests = query.order_by(LabTest.ordered_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('lab/list.html', lab_tests=lab_tests, status_filter=status_filter)

@app.route('/lab/add', methods=['GET', 'POST'])
@login_required
def add_lab_test():
    if request.method == 'POST':
        validator = validate_lab_test_form(request.form)
        
        if validator.is_valid():
            lab_test = LabTest()
            lab_test.test_id = generate_test_id()
            lab_test.patient_id = request.form['patient_id']
            lab_test.test_name = request.form['test_name']
            lab_test.test_type = request.form['test_type']
            lab_test.ordered_by = request.form['ordered_by']
            lab_test.normal_range = request.form.get('normal_range')
            lab_test.notes = request.form.get('notes')
            
            db.session.add(lab_test)
            db.session.commit()
            
            flash('Lab test ordered successfully!', 'success')
            return redirect(url_for('lab_list'))
        else:
            for field, error in validator.errors.items():
                flash(f'{field}: {error}', 'danger')
    
    patients = Patient.query.order_by(Patient.first_name).all()
    doctors = User.query.filter_by(role='doctor').order_by(User.first_name).all()
    
    return render_template('lab/add.html', patients=patients, doctors=doctors)

@app.route('/lab/<int:test_id>')
@login_required
def view_lab_test(test_id):
    lab_test = LabTest.query.get_or_404(test_id)
    return render_template('lab/view.html', lab_test=lab_test)

# Reports
@app.route('/reports')
@login_required
def reports():
    # Basic statistics for reports
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    total_revenue = db.session.query(db.func.sum(Bill.total_amount)).scalar() or 0
    pending_bills = Bill.query.filter_by(status='pending').count()
    
    # Monthly statistics
    current_month = datetime.now().replace(day=1)
    monthly_patients = Patient.query.filter(Patient.created_at >= current_month).count()
    monthly_revenue = db.session.query(db.func.sum(Bill.total_amount)).filter(
        Bill.bill_date >= current_month
    ).scalar() or 0
    
    return render_template('reports/index.html',
                         total_patients=total_patients,
                         total_appointments=total_appointments,
                         total_revenue=total_revenue,
                         pending_bills=pending_bills,
                         monthly_patients=monthly_patients,
                         monthly_revenue=monthly_revenue)

# Initialize admin user if no users exist
def create_admin():
    with app.app_context():
        if User.query.count() == 0:
            admin = User()
            admin.username = 'admin'
            admin.email = 'admin@hospital.com'
            admin.role = 'admin'
            admin.first_name = 'System'
            admin.last_name = 'Administrator'
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created: admin/admin123")
