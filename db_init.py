#!/usr/bin/env python3
"""
Database Initialization Script for Hospital Management System
"""
import os
import sys
from app import app, db
from models import User, Patient, Appointment, Bill, BillItem, LabTest

def init_database():
    """Initialize the database with tables and default data"""
    print("Initializing Hospital Management System Database...")
    
    with app.app_context():
        try:
            # Drop all tables (for fresh setup)
            print("Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            
            # Create default admin user
            print("Creating default admin user...")
            if User.query.count() == 0:
                admin = User()
                admin.username = 'admin'
                admin.email = 'admin@hospital.com'
                admin.role = 'admin'
                admin.first_name = 'System'
                admin.last_name = 'Administrator'
                admin.set_password('admin123')
                admin.is_active = True
                
                db.session.add(admin)
                
                # Create a sample doctor user
                doctor = User()
                doctor.username = 'dr.smith'
                doctor.email = 'dr.smith@hospital.com'
                doctor.role = 'doctor'
                doctor.first_name = 'John'
                doctor.last_name = 'Smith'
                doctor.set_password('doctor123')
                doctor.is_active = True
                
                db.session.add(doctor)
                
                # Create a sample staff user
                staff = User()
                staff.username = 'nurse.jane'
                staff.email = 'nurse.jane@hospital.com'
                staff.role = 'staff'
                staff.first_name = 'Jane'
                staff.last_name = 'Doe'
                staff.set_password('staff123')
                staff.is_active = True
                
                db.session.add(staff)
                
                db.session.commit()
                print("✓ Default users created:")
                print("  - Admin: admin / admin123")
                print("  - Doctor: dr.smith / doctor123")
                print("  - Staff: nurse.jane / staff123")
            
            # Verify database setup
            print("\nDatabase setup verification:")
            print(f"✓ Users table: {User.query.count()} users")
            print(f"✓ Patients table: {Patient.query.count()} patients") 
            print(f"✓ Appointments table: {Appointment.query.count()} appointments")
            print(f"✓ Bills table: {Bill.query.count()} bills")
            print(f"✓ Lab Tests table: {LabTest.query.count()} lab tests")
            
            # Show database connection info
            db_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if db_url.startswith('postgresql'):
                print(f"\n✓ Connected to PostgreSQL database")
            elif db_url.startswith('sqlite'):
                print(f"\n✓ Connected to SQLite database: {db_url}")
            else:
                print(f"\n✓ Connected to database: {db_url[:50]}...")
                
            print("\n🎉 Database initialization completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            import traceback
            traceback.print_exc()
            return False

def reset_database():
    """Reset the database (drop and recreate all tables)"""
    print("⚠️  RESETTING DATABASE - All data will be lost!")
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() == 'yes':
        return init_database()
    else:
        print("Database reset cancelled.")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    else:
        init_database()