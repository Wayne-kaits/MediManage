#!/usr/bin/env python3
"""
Database Management Tool for Hospital Management System
Provides utilities for database operations, backups, and maintenance
"""
import os
import sys
import json
from datetime import datetime, timedelta
from app import app, db
from models import User, Patient, Appointment, Bill, BillItem, LabTest

class DatabaseManager:
    def __init__(self):
        self.app = app
        self.db = db
    
    def get_database_info(self):
        """Get database connection information"""
        with self.app.app_context():
            db_url = self.app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if db_url.startswith('postgresql'):
                return {
                    'type': 'PostgreSQL',
                    'url': db_url,
                    'connection': 'Active' if self.test_connection() else 'Failed'
                }
            elif db_url.startswith('sqlite'):
                return {
                    'type': 'SQLite',
                    'url': db_url,
                    'connection': 'Active' if self.test_connection() else 'Failed'
                }
            else:
                return {
                    'type': 'Unknown',
                    'url': db_url,
                    'connection': 'Unknown'
                }
    
    def test_connection(self):
        """Test database connection"""
        try:
            with self.app.app_context():
                result = self.db.session.execute(self.db.text('SELECT 1'))
                return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def get_stats(self):
        """Get database statistics"""
        with self.app.app_context():
            try:
                stats = {
                    'users': User.query.count(),
                    'patients': Patient.query.count(),
                    'appointments': Appointment.query.count(),
                    'bills': Bill.query.count(),
                    'bill_items': BillItem.query.count(),
                    'lab_tests': LabTest.query.count(),
                    'total_revenue': self.db.session.query(self.db.func.sum(Bill.total_amount)).scalar() or 0,
                    'pending_bills': Bill.query.filter_by(status='pending').count(),
                    'completed_appointments': Appointment.query.filter_by(status='completed').count(),
                    'pending_lab_tests': LabTest.query.filter_by(status='pending').count(),
                }
                return stats
            except Exception as e:
                print(f"Error getting stats: {e}")
                return {}
    
    def backup_data(self, output_file=None):
        """Create a JSON backup of all data"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'backup_hospital_db_{timestamp}.json'
        
        with self.app.app_context():
            try:
                backup_data = {
                    'timestamp': datetime.now().isoformat(),
                    'database_type': self.get_database_info()['type'],
                    'users': [],
                    'patients': [],
                    'appointments': [],
                    'bills': [],
                    'bill_items': [],
                    'lab_tests': []
                }
                
                # Backup users (without passwords)
                for user in User.query.all():
                    backup_data['users'].append({
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'created_at': user.created_at.isoformat() if user.created_at else None,
                        'is_active': user.is_active
                    })
                
                # Backup patients
                for patient in Patient.query.all():
                    backup_data['patients'].append({
                        'id': patient.id,
                        'patient_id': patient.patient_id,
                        'first_name': patient.first_name,
                        'last_name': patient.last_name,
                        'date_of_birth': patient.date_of_birth.isoformat() if patient.date_of_birth else None,
                        'gender': patient.gender,
                        'phone': patient.phone,
                        'email': patient.email,
                        'address': patient.address,
                        'emergency_contact': patient.emergency_contact,
                        'emergency_phone': patient.emergency_phone,
                        'blood_type': patient.blood_type,
                        'allergies': patient.allergies,
                        'medical_history': patient.medical_history,
                        'created_at': patient.created_at.isoformat() if patient.created_at else None
                    })
                
                # Backup appointments
                for appointment in Appointment.query.all():
                    backup_data['appointments'].append({
                        'id': appointment.id,
                        'patient_id': appointment.patient_id,
                        'doctor_id': appointment.doctor_id,
                        'appointment_date': appointment.appointment_date.isoformat() if appointment.appointment_date else None,
                        'appointment_type': appointment.appointment_type,
                        'status': appointment.status,
                        'notes': appointment.notes,
                        'created_at': appointment.created_at.isoformat() if appointment.created_at else None
                    })
                
                # Backup bills
                for bill in Bill.query.all():
                    backup_data['bills'].append({
                        'id': bill.id,
                        'bill_number': bill.bill_number,
                        'patient_id': bill.patient_id,
                        'appointment_id': bill.appointment_id,
                        'total_amount': bill.total_amount,
                        'paid_amount': bill.paid_amount,
                        'status': bill.status,
                        'bill_date': bill.bill_date.isoformat() if bill.bill_date else None,
                        'due_date': bill.due_date.isoformat() if bill.due_date else None,
                        'notes': bill.notes,
                        'created_at': bill.created_at.isoformat() if bill.created_at else None
                    })
                
                # Backup bill items
                for item in BillItem.query.all():
                    backup_data['bill_items'].append({
                        'id': item.id,
                        'bill_id': item.bill_id,
                        'description': item.description,
                        'quantity': item.quantity,
                        'unit_price': item.unit_price,
                        'total_price': item.total_price
                    })
                
                # Backup lab tests
                for test in LabTest.query.all():
                    backup_data['lab_tests'].append({
                        'id': test.id,
                        'test_id': test.test_id,
                        'patient_id': test.patient_id,
                        'test_name': test.test_name,
                        'test_type': test.test_type,
                        'ordered_by': test.ordered_by,
                        'status': test.status,
                        'results': test.results,
                        'normal_range': test.normal_range,
                        'notes': test.notes,
                        'ordered_date': test.ordered_date.isoformat() if test.ordered_date else None,
                        'completed_date': test.completed_date.isoformat() if test.completed_date else None
                    })
                
                # Write backup file
                with open(output_file, 'w') as f:
                    json.dump(backup_data, f, indent=2, default=str)
                
                print(f"✓ Database backup created: {output_file}")
                print(f"  - Users: {len(backup_data['users'])}")
                print(f"  - Patients: {len(backup_data['patients'])}")
                print(f"  - Appointments: {len(backup_data['appointments'])}")
                print(f"  - Bills: {len(backup_data['bills'])}")
                print(f"  - Lab Tests: {len(backup_data['lab_tests'])}")
                
                return True
                
            except Exception as e:
                print(f"❌ Error creating backup: {e}")
                return False
    
    def cleanup_old_data(self, days_old=90):
        """Clean up old completed appointments and paid bills"""
        with self.app.app_context():
            try:
                cutoff_date = datetime.now() - timedelta(days=days_old)
                
                # Count items to be cleaned
                old_appointments = Appointment.query.filter(
                    Appointment.status == 'completed',
                    Appointment.updated_at < cutoff_date
                ).count()
                
                old_bills = Bill.query.filter(
                    Bill.status == 'paid',
                    Bill.created_at < cutoff_date
                ).count()
                
                print(f"Found {old_appointments} old completed appointments")
                print(f"Found {old_bills} old paid bills")
                
                if old_appointments == 0 and old_bills == 0:
                    print("No old data to clean up.")
                    return True
                
                # Ask for confirmation
                response = input(f"Delete {old_appointments + old_bills} old records? (yes/no): ")
                if response.lower() != 'yes':
                    print("Cleanup cancelled.")
                    return False
                
                # Perform cleanup (this is a placeholder - implement carefully)
                print("⚠️  Data cleanup would be implemented here with proper foreign key handling")
                print("This feature requires careful implementation to maintain data integrity.")
                
                return True
                
            except Exception as e:
                print(f"❌ Error during cleanup: {e}")
                return False
    
    def show_status(self):
        """Show comprehensive database status"""
        print("=" * 60)
        print("HOSPITAL MANAGEMENT SYSTEM - DATABASE STATUS")
        print("=" * 60)
        
        # Database connection info
        db_info = self.get_database_info()
        print(f"Database Type: {db_info['type']}")
        print(f"Connection Status: {db_info['connection']}")
        print(f"Database URL: {db_info['url'][:50]}..." if len(db_info['url']) > 50 else f"Database URL: {db_info['url']}")
        
        print("\n" + "-" * 40)
        print("DATABASE STATISTICS")
        print("-" * 40)
        
        stats = self.get_stats()
        if stats:
            print(f"👥 Users: {stats['users']}")
            print(f"🏥 Patients: {stats['patients']}")
            print(f"📅 Appointments: {stats['appointments']} (Completed: {stats['completed_appointments']})")
            print(f"💰 Bills: {stats['bills']} (Pending: {stats['pending_bills']})")
            print(f"🧪 Lab Tests: {stats['lab_tests']} (Pending: {stats['pending_lab_tests']})")
            print(f"💵 Total Revenue: ${stats['total_revenue']:.2f}")
        else:
            print("Unable to retrieve statistics")
        
        print("\n" + "=" * 60)

def main():
    dm = DatabaseManager()
    
    if len(sys.argv) < 2:
        print("Hospital Management System - Database Manager")
        print("\nUsage:")
        print("  python database_manager.py status      - Show database status")
        print("  python database_manager.py backup      - Create database backup")
        print("  python database_manager.py cleanup     - Clean up old data")
        print("  python database_manager.py test        - Test database connection")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'status':
        dm.show_status()
    elif command == 'backup':
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        dm.backup_data(output_file)
    elif command == 'cleanup':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 90
        dm.cleanup_old_data(days)
    elif command == 'test':
        if dm.test_connection():
            print("✓ Database connection successful")
        else:
            print("❌ Database connection failed")
    else:
        print(f"Unknown command: {command}")

if __name__ == '__main__':
    main()