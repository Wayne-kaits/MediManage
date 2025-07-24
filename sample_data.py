#!/usr/bin/env python3
"""
Sample Data Generator for Hospital Management System
"""
from datetime import datetime, date, timedelta
from app import app, db
from models import User, Patient, Appointment, Bill, BillItem, LabTest
from utils import generate_patient_id, generate_bill_number, generate_test_id

def add_sample_data():
    """Add sample data for demonstration"""
    print("Adding sample data to Hospital Management System...")
    
    with app.app_context():
        try:
            # Add sample patients
            patients_data = [
                {
                    'first_name': 'Alice',
                    'last_name': 'Johnson',
                    'date_of_birth': date(1985, 3, 15),
                    'gender': 'Female',
                    'phone': '(555) 123-4567',
                    'email': 'alice.johnson@email.com',
                    'address': '123 Main St, Anytown, ST 12345',
                    'emergency_contact': 'Bob Johnson',
                    'emergency_phone': '(555) 987-6543',
                    'blood_type': 'A+',
                    'allergies': 'Penicillin',
                    'medical_history': 'Hypertension, controlled with medication'
                },
                {
                    'first_name': 'Michael',
                    'last_name': 'Brown',
                    'date_of_birth': date(1972, 8, 22),
                    'gender': 'Male',
                    'phone': '(555) 234-5678',
                    'email': 'michael.brown@email.com',
                    'address': '456 Oak Ave, Springfield, ST 67890',
                    'emergency_contact': 'Sarah Brown',
                    'emergency_phone': '(555) 876-5432',
                    'blood_type': 'O-',
                    'allergies': 'None known',
                    'medical_history': 'Diabetes Type 2, regular checkups'
                },
                {
                    'first_name': 'Emma',
                    'last_name': 'Davis',
                    'date_of_birth': date(1990, 12, 5),
                    'gender': 'Female',
                    'phone': '(555) 345-6789',
                    'email': 'emma.davis@email.com',
                    'address': '789 Pine Rd, Riverside, ST 11223',
                    'emergency_contact': 'James Davis',
                    'emergency_phone': '(555) 765-4321',
                    'blood_type': 'B+',
                    'allergies': 'Shellfish',
                    'medical_history': 'Asthma, uses inhaler as needed'
                }
            ]
            
            created_patients = []
            for patient_data in patients_data:
                patient = Patient()
                patient.patient_id = generate_patient_id()
                for key, value in patient_data.items():
                    setattr(patient, key, value)
                
                db.session.add(patient)
                created_patients.append(patient)
            
            db.session.flush()  # Get patient IDs
            print(f"✓ Added {len(created_patients)} sample patients")
            
            # Add sample appointments
            doctor = User.query.filter_by(role='doctor').first()
            if doctor and created_patients:
                appointments_data = [
                    {
                        'patient_id': created_patients[0].id,
                        'doctor_id': doctor.id,
                        'appointment_date': datetime.now() + timedelta(days=1, hours=10),
                        'appointment_type': 'Regular Checkup',
                        'notes': 'Annual physical examination',
                        'status': 'scheduled'
                    },
                    {
                        'patient_id': created_patients[1].id,
                        'doctor_id': doctor.id,
                        'appointment_date': datetime.now() + timedelta(days=3, hours=14),
                        'appointment_type': 'Follow-up',
                        'notes': 'Diabetes monitoring',
                        'status': 'scheduled'
                    },
                    {
                        'patient_id': created_patients[2].id,
                        'doctor_id': doctor.id,
                        'appointment_date': datetime.now() - timedelta(days=7, hours=-9),
                        'appointment_type': 'Consultation',
                        'notes': 'Asthma evaluation',
                        'status': 'completed'
                    }
                ]
                
                created_appointments = []
                for apt_data in appointments_data:
                    appointment = Appointment()
                    for key, value in apt_data.items():
                        setattr(appointment, key, value)
                    
                    db.session.add(appointment)
                    created_appointments.append(appointment)
                
                db.session.flush()
                print(f"✓ Added {len(created_appointments)} sample appointments")
                
                # Add sample bills
                bills_data = [
                    {
                        'patient_id': created_patients[0].id,
                        'appointment_id': created_appointments[0].id,
                        'total_amount': 250.00,
                        'due_date': datetime.now().date() + timedelta(days=30),
                        'status': 'pending',
                        'notes': 'Annual checkup charges'
                    },
                    {
                        'patient_id': created_patients[2].id,
                        'appointment_id': created_appointments[2].id,
                        'total_amount': 180.00,
                        'due_date': datetime.now().date() + timedelta(days=15),
                        'status': 'paid',
                        'notes': 'Consultation and medication'
                    }
                ]
                
                for bill_data in bills_data:
                    bill = Bill()
                    bill.bill_number = generate_bill_number()
                    for key, value in bill_data.items():
                        setattr(bill, key, value)
                    
                    db.session.add(bill)
                    db.session.flush()
                    
                    # Add bill items
                    if bill_data['status'] == 'pending':
                        # Checkup bill items
                        items = [
                            {'description': 'Consultation Fee', 'quantity': 1, 'unit_price': 150.00},
                            {'description': 'Blood Pressure Check', 'quantity': 1, 'unit_price': 50.00},
                            {'description': 'Basic Health Screening', 'quantity': 1, 'unit_price': 50.00}
                        ]
                    else:
                        # Consultation bill items
                        items = [
                            {'description': 'Specialist Consultation', 'quantity': 1, 'unit_price': 120.00},
                            {'description': 'Breathing Assessment', 'quantity': 1, 'unit_price': 60.00}
                        ]
                    
                    for item_data in items:
                        bill_item = BillItem()
                        bill_item.bill_id = bill.id
                        bill_item.description = item_data['description']
                        bill_item.quantity = item_data['quantity']
                        bill_item.unit_price = item_data['unit_price']
                        bill_item.total_price = item_data['quantity'] * item_data['unit_price']
                        
                        db.session.add(bill_item)
                
                print(f"✓ Added {len(bills_data)} sample bills with items")
                
                # Add sample lab tests
                lab_tests_data = [
                    {
                        'patient_id': created_patients[0].id,
                        'test_name': 'Complete Blood Count',
                        'test_type': 'Blood Test',
                        'ordered_by': doctor.id,
                        'status': 'completed',
                        'normal_range': 'WBC: 4.5-11.0, RBC: 4.5-5.9, Hemoglobin: 12-16',
                        'results': 'WBC: 7.2, RBC: 4.8, Hemoglobin: 14.2 - All values within normal range',
                        'notes': 'Regular health screening'
                    },
                    {
                        'patient_id': created_patients[1].id,
                        'test_name': 'HbA1c Test',
                        'test_type': 'Blood Test',
                        'ordered_by': doctor.id,
                        'status': 'pending',
                        'normal_range': 'Less than 7% for diabetic patients',
                        'notes': 'Diabetes monitoring'
                    },
                    {
                        'patient_id': created_patients[2].id,
                        'test_name': 'Pulmonary Function Test',
                        'test_type': 'Respiratory Test',
                        'ordered_by': doctor.id,
                        'status': 'in_progress',
                        'normal_range': 'FEV1: 80-120% predicted',
                        'notes': 'Asthma assessment'
                    }
                ]
                
                for lab_data in lab_tests_data:
                    lab_test = LabTest()
                    lab_test.test_id = generate_test_id()
                    for key, value in lab_data.items():
                        setattr(lab_test, key, value)
                    
                    db.session.add(lab_test)
                
                print(f"✓ Added {len(lab_tests_data)} sample lab tests")
            
            db.session.commit()
            
            # Final verification
            print("\nSample data summary:")
            print(f"✓ Total Patients: {Patient.query.count()}")
            print(f"✓ Total Appointments: {Appointment.query.count()}")
            print(f"✓ Total Bills: {Bill.query.count()}")
            print(f"✓ Total Lab Tests: {LabTest.query.count()}")
            print(f"✓ Total Users: {User.query.count()}")
            
            print("\n🎉 Sample data added successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error adding sample data: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    add_sample_data()