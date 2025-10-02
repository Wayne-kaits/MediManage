"""
Advanced analytics module for MediManage
Provides data analysis, visualization, and predictive capabilities
"""

from datetime import datetime, timedelta
import json
import pandas as pd
import numpy as np
from sqlalchemy import func, extract, and_, or_, case, text
from db import db
from models import Patient, Appointment, Bill, BillItem, LabTest, User
from security import log_audit

class Analytics:
    """Analytics class for generating insights from hospital data"""
    
    @staticmethod
    def get_patient_demographics():
        """Get patient demographics data for visualization"""
        # Age distribution
        current_year = datetime.now().year
        age_groups = {
            '0-17': 0,
            '18-30': 0,
            '31-45': 0,
            '46-60': 0,
            '61-75': 0,
            '76+': 0
        }
        
        # Gender distribution
        gender_counts = {
            'Male': 0,
            'Female': 0,
            'Other': 0
        }
        
        # Blood type distribution
        blood_types = {
            'A+': 0, 'A-': 0,
            'B+': 0, 'B-': 0,
            'AB+': 0, 'AB-': 0,
            'O+': 0, 'O-': 0,
            'Unknown': 0
        }
        
        # Use optimized query with aggregation
        patients = db.session.query(
            Patient.date_of_birth,
            Patient.gender,
            Patient.blood_type
        ).all()
        
        for patient in patients:
            # Calculate age
            if patient.date_of_birth:
                age = current_year - patient.date_of_birth.year
                if age <= 17:
                    age_groups['0-17'] += 1
                elif age <= 30:
                    age_groups['18-30'] += 1
                elif age <= 45:
                    age_groups['31-45'] += 1
                elif age <= 60:
                    age_groups['46-60'] += 1
                elif age <= 75:
                    age_groups['61-75'] += 1
                else:
                    age_groups['76+'] += 1
            
            # Gender
            gender = patient.gender.capitalize() if patient.gender else 'Other'
            if gender in gender_counts:
                gender_counts[gender] += 1
            else:
                gender_counts['Other'] += 1
            
            # Blood type
            blood_type = patient.blood_type if patient.blood_type else 'Unknown'
            if blood_type in blood_types:
                blood_types[blood_type] += 1
            else:
                blood_types['Unknown'] += 1
        
        return {
            'age_groups': age_groups,
            'gender_counts': gender_counts,
            'blood_types': blood_types
        }
    
    @staticmethod
    def get_appointment_trends(days=30):
        """Get appointment trends over time"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Optimized query with aggregation
        appointments = db.session.query(
            Appointment.appointment_date,
            Appointment.status,
            Appointment.appointment_type
        ).filter(
            Appointment.appointment_date >= start_date,
            Appointment.appointment_date <= end_date
        ).all()
        
        # Prepare data structure
        date_range = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') 
                     for i in range(days + 1)]
        
        appointment_counts = {date: 0 for date in date_range}
        status_counts = {
            'scheduled': 0,
            'completed': 0,
            'cancelled': 0
        }
        type_counts = {}
        
        # Process appointments
        for appointment in appointments:
            date_str = appointment.appointment_date.strftime('%Y-%m-%d')
            if date_str in appointment_counts:
                appointment_counts[date_str] += 1
            
            # Status counts
            status = appointment.status.lower()
            if status in status_counts:
                status_counts[status] += 1
            
            # Type counts
            app_type = appointment.appointment_type
            if app_type in type_counts:
                type_counts[app_type] += 1
            else:
                type_counts[app_type] = 1
        
        return {
            'daily_counts': appointment_counts,
            'status_distribution': status_counts,
            'type_distribution': type_counts
        }
    
    @staticmethod
    def get_revenue_analytics(months=12):
        """Get revenue analytics over time"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30*months)
        
        # Optimized query with aggregation
        bills = db.session.query(
            Bill.bill_date,
            Bill.status,
            Bill.total_amount,
            Bill.balance
        ).filter(
            Bill.bill_date >= start_date,
            Bill.bill_date <= end_date
        ).all()
        
        # Prepare data structure
        monthly_revenue = {}
        payment_status = {
            'paid': 0,
            'partial': 0,
            'pending': 0,
            'overdue': 0
        }
        
        # Process bills
        total_revenue = 0
        outstanding_amount = 0
        
        for bill in bills:
            # Monthly revenue
            month_key = bill.bill_date.strftime('%Y-%m')
            if month_key in monthly_revenue:
                monthly_revenue[month_key] += bill.total_amount
            else:
                monthly_revenue[month_key] = bill.total_amount
            
            # Payment status
            status = bill.status.lower()
            if status in payment_status:
                payment_status[status] += 1
            
            # Totals
            total_revenue += bill.total_amount
            outstanding_amount += bill.balance
        
        # Sort monthly revenue by date
        sorted_monthly_revenue = {k: monthly_revenue[k] for k in sorted(monthly_revenue.keys())}
        
        return {
            'monthly_revenue': sorted_monthly_revenue,
            'payment_status': payment_status,
            'total_revenue': total_revenue,
            'outstanding_amount': outstanding_amount,
            'collection_rate': (total_revenue - outstanding_amount) / total_revenue if total_revenue > 0 else 0
        }
    
    @staticmethod
    def get_lab_test_analytics():
        """Get analytics on lab tests"""
        # Optimized query with aggregation
        lab_tests = db.session.query(
            LabTest.test_type,
            LabTest.status
        ).all()
        
        # Prepare data structure
        test_type_counts = {}
        status_counts = {
            'ordered': 0,
            'in_progress': 0,
            'completed': 0
        }
        
        # Process lab tests
        for test in lab_tests:
            # Test type counts
            test_type = test.test_type
            if test_type in test_type_counts:
                test_type_counts[test_type] += 1
            else:
                test_type_counts[test_type] = 1
            
            # Status counts
            status = test.status.lower()
            if status in status_counts:
                status_counts[status] += 1
        
        return {
            'test_type_distribution': test_type_counts,
            'status_distribution': status_counts
        }
    
    @staticmethod
    def get_doctor_performance():
        """Get performance metrics for doctors"""
        # Get all doctors with optimized query
        doctors = User.query.filter_by(role='doctor').all()
        
        doctor_metrics = {}
        
        for doctor in doctors:
            # Get appointments for this doctor with optimized query
            appointment_stats = db.session.query(
                func.count(Appointment.id).label('total'),
                func.sum(case([(Appointment.status == 'completed', 1)], else_=0)).label('completed'),
                func.sum(case([(Appointment.status == 'cancelled', 1)], else_=0)).label('cancelled')
            ).filter(Appointment.doctor_id == doctor.id).first()
            
            # Get lab tests ordered by this doctor
            lab_tests_count = LabTest.query.filter_by(ordered_by=doctor.id).count()
            
            # Calculate completion rate
            total_appointments = appointment_stats.total or 0
            completed_appointments = appointment_stats.completed or 0
            cancelled_appointments = appointment_stats.cancelled or 0
            
            completion_rate = completed_appointments / total_appointments if total_appointments > 0 else 0
            
            doctor_metrics[doctor.id] = {
                'name': f"Dr. {doctor.first_name} {doctor.last_name}",
                'total_appointments': total_appointments,
                'completed_appointments': completed_appointments,
                'cancelled_appointments': cancelled_appointments,
                'lab_tests_ordered': lab_tests_count,
                'completion_rate': completion_rate
            }
        
        return doctor_metrics
    
    @staticmethod
    def predict_appointment_load(days_ahead=7):
        """Predict appointment load for coming days based on historical patterns"""
        # Get historical appointment data with optimized query
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)  # Use 90 days of history
        
        appointments = db.session.query(
            Appointment.appointment_date
        ).filter(
            Appointment.appointment_date >= start_date,
            Appointment.appointment_date <= end_date
        ).all()
        
        # Convert to DataFrame for analysis
        appointment_dates = [a.appointment_date for a in appointments]
        df = pd.DataFrame({'date': appointment_dates})
        
        # Extract day of week
        df['day_of_week'] = df['date'].apply(lambda x: x.weekday())
        
        # Calculate average appointments by day of week
        day_averages = df.groupby('day_of_week').size().reset_index(name='count')
        day_averages['average'] = day_averages['count'] / 13  # 90/7 ~= 13 weeks
        
        # Generate predictions for next days_ahead days
        predictions = {}
        for i in range(days_ahead):
            future_date = end_date + timedelta(days=i+1)
            day_of_week = future_date.weekday()
            
            # Get average for this day of week
            avg_appointments = day_averages[day_averages['day_of_week'] == day_of_week]['average'].values
            if len(avg_appointments) > 0:
                predicted = avg_appointments[0]
            else:
                predicted = 0
            
            # Add some randomness based on recent trends
            recent_variance = np.std([len(df[df['date'].dt.date == (end_date - timedelta(days=j)).date()]) 
                                    for j in range(1, 8)])
            
            # Adjust prediction with some randomness
            adjusted_prediction = max(0, predicted + np.random.normal(0, recent_variance/2))
            
            predictions[future_date.strftime('%Y-%m-%d')] = round(adjusted_prediction)
        
        return predictions
    
    @staticmethod
    def get_patient_visit_frequency():
        """Analyze how frequently patients visit the hospital"""
        # Optimized query with aggregation
        patient_visit_counts = db.session.query(
            Appointment.patient_id,
            func.count(Appointment.id).label('visit_count')
        ).group_by(Appointment.patient_id).all()
        
        # Calculate visit frequency
        frequency_distribution = {
            '1 visit': 0,
            '2-3 visits': 0,
            '4-5 visits': 0,
            '6-10 visits': 0,
            '11+ visits': 0
        }
        
        for patient_id, visit_count in patient_visit_counts:
            if visit_count == 1:
                frequency_distribution['1 visit'] += 1
            elif visit_count <= 3:
                frequency_distribution['2-3 visits'] += 1
            elif visit_count <= 5:
                frequency_distribution['4-5 visits'] += 1
            elif visit_count <= 10:
                frequency_distribution['6-10 visits'] += 1
            else:
                frequency_distribution['11+ visits'] += 1
        
        return frequency_distribution
    
    @staticmethod
    def get_dashboard_summary():
        """Get a summary of key metrics for the dashboard"""
        # Patient metrics with optimized queries
        total_patients = Patient.query.count()
        new_patients_30d = Patient.query.filter(
            Patient.created_at >= datetime.now() - timedelta(days=30)
        ).count()
        
        # Appointment metrics with optimized queries
        total_appointments = Appointment.query.count()
        upcoming_appointments = Appointment.query.filter(
            Appointment.appointment_date >= datetime.now(),
            Appointment.status == 'scheduled'
        ).count()
        
        # Revenue metrics with optimized queries
        total_revenue = db.session.query(func.sum(Bill.total_amount)).scalar() or 0
        outstanding_amount = db.session.query(func.sum(Bill.balance)).scalar() or 0
        
        # Lab metrics with optimized queries
        pending_labs = LabTest.query.filter(
            LabTest.status != 'completed'
        ).count()
        
        return {
            'patient_metrics': {
                'total_patients': total_patients,
                'new_patients_30d': new_patients_30d,
                'patient_growth_rate': (new_patients_30d / total_patients) if total_patients > 0 else 0
            },
            'appointment_metrics': {
                'total_appointments': total_appointments,
                'upcoming_appointments': upcoming_appointments
            },
            'revenue_metrics': {
                'total_revenue': total_revenue,
                'outstanding_amount': outstanding_amount,
                'collection_rate': (total_revenue - outstanding_amount) / total_revenue if total_revenue > 0 else 0
            },
            'lab_metrics': {
                'pending_labs': pending_labs
            }
        }
    
    @staticmethod
    def get_financial_insights():
        """Get financial insights and trends"""
        # Revenue by service type
        revenue_by_service = db.session.query(
            BillItem.service_type,
            func.sum(BillItem.amount).label('total_amount')
        ).group_by(BillItem.service_type).all()
        
        service_revenue = {service: amount for service, amount in revenue_by_service}
        
        # Average bill amount
        avg_bill_amount = db.session.query(func.avg(Bill.total_amount)).scalar() or 0
        
        # Payment method distribution
        payment_methods = db.session.query(
            Bill.payment_method,
            func.count(Bill.id).label('count')
        ).filter(Bill.payment_method != None).group_by(Bill.payment_method).all()
        
        payment_method_counts = {method: count for method, count in payment_methods}
        
        # Outstanding balances by age
        current_date = datetime.now()
        
        # 0-30 days
        balance_0_30 = db.session.query(func.sum(Bill.balance)).filter(
            Bill.bill_date >= current_date - timedelta(days=30),
            Bill.balance > 0
        ).scalar() or 0
        
        # 31-60 days
        balance_31_60 = db.session.query(func.sum(Bill.balance)).filter(
            Bill.bill_date >= current_date - timedelta(days=60),
            Bill.bill_date < current_date - timedelta(days=30),
            Bill.balance > 0
        ).scalar() or 0
        
        # 61-90 days
        balance_61_90 = db.session.query(func.sum(Bill.balance)).filter(
            Bill.bill_date >= current_date - timedelta(days=90),
            Bill.bill_date < current_date - timedelta(days=60),
            Bill.balance > 0
        ).scalar() or 0
        
        # >90 days
        balance_over_90 = db.session.query(func.sum(Bill.balance)).filter(
            Bill.bill_date < current_date - timedelta(days=90),
            Bill.balance > 0
        ).scalar() or 0
        
        return {
            'service_revenue': service_revenue,
            'avg_bill_amount': avg_bill_amount,
            'payment_methods': payment_method_counts,
            'outstanding_by_age': {
                '0-30 days': balance_0_30,
                '31-60 days': balance_31_60,
                '61-90 days': balance_61_90,
                'Over 90 days': balance_over_90
            }
        }
    
    @staticmethod
    def get_operational_insights():
        """Get operational insights for hospital management"""
        # Busiest days of week
        busiest_days = db.session.query(
            extract('dow', Appointment.appointment_date).label('day_of_week'),
            func.count(Appointment.id).label('count')
        ).group_by('day_of_week').order_by(text('count DESC')).all()
        
        days_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
                   4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        
        busiest_days_data = {days_map[day]: count for day, count in busiest_days}
        
        # Busiest hours
        busiest_hours = db.session.query(
            extract('hour', Appointment.appointment_time).label('hour'),
            func.count(Appointment.id).label('count')
        ).group_by('hour').order_by(text('count DESC')).all()
        
        busiest_hours_data = {f"{hour}:00": count for hour, count in busiest_hours}
        
        # Average appointment duration
        avg_duration = db.session.query(
            func.avg(Appointment.duration)
        ).filter(Appointment.duration != None).scalar() or 0
        
        # No-show rate
        total_appointments = Appointment.query.filter(
            Appointment.appointment_date < datetime.now()
        ).count()
        
        no_shows = Appointment.query.filter(
            Appointment.appointment_date < datetime.now(),
            Appointment.status == 'no_show'
        ).count()
        
        no_show_rate = no_shows / total_appointments if total_appointments > 0 else 0
        
        return {
            'busiest_days': busiest_days_data,
            'busiest_hours': busiest_hours_data,
            'avg_appointment_duration': avg_duration,
            'no_show_rate': no_show_rate
        }
    
    @staticmethod
    def export_data_for_analysis(start_date=None, end_date=None):
        """Export data for external analysis"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now()
        
        # Log the export
        log_audit(None, 'data_export', 'analytics', None, 
                 f"Data exported for analysis from {start_date} to {end_date}")
        
        # Patient data (anonymized)
        patients_data = []
        patients = Patient.query.all()
        for patient in patients:
            patients_data.append({
                'id': patient.id,
                'age': datetime.now().year - patient.date_of_birth.year if patient.date_of_birth else None,
                'gender': patient.gender,
                'blood_type': patient.blood_type
            })
        
        # Appointment data
        appointments_data = []
        appointments = Appointment.query.filter(
            Appointment.appointment_date >= start_date,
            Appointment.appointment_date <= end_date
        ).all()
        
        for appointment in appointments:
            appointments_data.append({
                'id': appointment.id,
                'patient_id': appointment.patient_id,
                'doctor_id': appointment.doctor_id,
                'date': appointment.appointment_date.strftime('%Y-%m-%d'),
                'time': appointment.appointment_time.strftime('%H:%M') if appointment.appointment_time else None,
                'type': appointment.appointment_type,
                'status': appointment.status,
                'duration': appointment.duration
            })
        
        # Billing data
        billing_data = []
        bills = Bill.query.filter(
            Bill.bill_date >= start_date,
            Bill.bill_date <= end_date
        ).all()
        
        for bill in bills:
            billing_data.append({
                'id': bill.id,
                'patient_id': bill.patient_id,
                'date': bill.bill_date.strftime('%Y-%m-%d'),
                'total_amount': bill.total_amount,
                'paid_amount': bill.paid_amount,
                'balance': bill.balance,
                'status': bill.status,
                'payment_method': bill.payment_method
            })
        
        # Lab data
        lab_data = []
        lab_tests = LabTest.query.filter(
            LabTest.ordered_date >= start_date,
            LabTest.ordered_date <= end_date
        ).all()
        
        for test in lab_tests:
            lab_data.append({
                'id': test.id,
                'patient_id': test.patient_id,
                'ordered_by': test.ordered_by,
                'date': test.ordered_date.strftime('%Y-%m-%d'),
                'type': test.test_type,
                'status': test.status
            })
        
        return {
            'patients': patients_data,
            'appointments': appointments_data,
            'billing': billing_data,
            'lab_tests': lab_data
        }