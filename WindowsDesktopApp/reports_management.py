"""
Reports Management Module
Advanced reporting system with charts and analytics
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from desktop_app import ModernWidget, ModernStyle

class ReportsManagement:
    """Reports management interface"""
    
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        
        self.create_interface()
    
    def create_interface(self):
        """Create reports management interface"""
        # Title
        title_frame = ModernWidget.create_frame(self.parent)
        title_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ModernWidget.create_label(title_frame, "Reports & Analytics", size="title")
        title_label.pack(side="left")
        
        # Export button
        export_btn = ModernWidget.create_button(title_frame, "📊 Export Report", self.export_report, style="info")
        export_btn.pack(side="right")
        
        # Create notebook for different report types
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Dashboard tab
        dashboard_tab = ModernWidget.create_frame(self.notebook)
        self.notebook.add(dashboard_tab, text="📊 Dashboard")
        
        # Patient reports tab
        patient_tab = ModernWidget.create_frame(self.notebook)
        self.notebook.add(patient_tab, text="👥 Patient Reports")
        
        # Appointment reports tab
        appointment_tab = ModernWidget.create_frame(self.notebook)
        self.notebook.add(appointment_tab, text="📅 Appointment Reports")
        
        # Financial reports tab
        financial_tab = ModernWidget.create_frame(self.notebook)
        self.notebook.add(financial_tab, text="💰 Financial Reports")
        
        # Lab reports tab
        lab_tab = ModernWidget.create_frame(self.notebook)
        self.notebook.add(lab_tab, text="🧪 Lab Reports")
        
        # Create report interfaces
        self.create_dashboard_tab(dashboard_tab)
        self.create_patient_tab(patient_tab)
        self.create_appointment_tab(appointment_tab)
        self.create_financial_tab(financial_tab)
        self.create_lab_tab(lab_tab)
    
    def create_dashboard_tab(self, parent):
        """Create dashboard overview tab"""
        # Statistics cards
        stats_frame = ModernWidget.create_frame(parent)
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        # Get statistics
        stats = self.get_dashboard_stats()
        
        # Create stat cards
        stat_items = [
            ("Total Patients", stats['total_patients'], ModernStyle.BTN_PRIMARY),
            ("This Month Appointments", stats['month_appointments'], ModernStyle.BG_SUCCESS),
            ("Pending Bills", stats['pending_bills'], ModernStyle.BG_WARNING),
            ("Completed Tests", stats['completed_tests'], ModernStyle.BG_INFO)
        ]
        
        for i, (title, value, color) in enumerate(stat_items):
            card = tk.Frame(
                stats_frame,
                bg=color,
                relief="flat",
                borderwidth=0,
                width=250,
                height=120
            )
            card.pack(side="left", padx=10, fill="y")
            card.pack_propagate(False)
            
            value_label = tk.Label(
                card,
                text=str(value),
                bg=color,
                fg=ModernStyle.TEXT_PRIMARY,
                font=(ModernStyle.FONT_FAMILY, 24, "bold")
            )
            value_label.pack(pady=(20, 5))
            
            title_label = tk.Label(
                card,
                text=title,
                bg=color,
                fg=ModernStyle.TEXT_PRIMARY,
                font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL)
            )
            title_label.pack()
        
        # Charts frame
        charts_frame = ModernWidget.create_frame(parent)
        charts_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left chart - Monthly appointments
        left_chart_frame = ModernWidget.create_card(charts_frame, "Monthly Appointments Trend")
        left_chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.create_appointments_chart(left_chart_frame)
        
        # Right chart - Revenue trend
        right_chart_frame = ModernWidget.create_card(charts_frame, "Monthly Revenue")
        right_chart_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.create_revenue_chart(right_chart_frame)
    
    def create_patient_tab(self, parent):
        """Create patient reports tab"""
        # Filter frame
        filter_frame = ModernWidget.create_frame(parent)
        filter_frame.pack(fill="x", padx=20, pady=20)
        
        # Date range
        date_label = ModernWidget.create_label(filter_frame, "Registration Date Range:")
        date_label.pack(side="left", padx=(0, 10))
        
        self.patient_start_date = DateEntry(
            filter_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.patient_start_date.pack(side="left", padx=(0, 5))
        
        to_label = ModernWidget.create_label(filter_frame, "to")
        to_label.pack(side="left", padx=5)
        
        self.patient_end_date = DateEntry(
            filter_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.patient_end_date.pack(side="left", padx=(5, 20))
        
        generate_btn = ModernWidget.create_button(
            filter_frame, 
            "📊 Generate Report", 
            self.generate_patient_report, 
            style="primary"
        )
        generate_btn.pack(side="left")
        
        # Report display frame
        self.patient_report_frame = ModernWidget.create_card(parent, "Patient Report")
        self.patient_report_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Initial report
        self.generate_patient_report()
    
    def create_appointment_tab(self, parent):
        """Create appointment reports tab"""
        # Filter frame
        filter_frame = ModernWidget.create_frame(parent)
        filter_frame.pack(fill="x", padx=20, pady=20)
        
        # Date range
        date_label = ModernWidget.create_label(filter_frame, "Appointment Date Range:")
        date_label.pack(side="left", padx=(0, 10))
        
        self.apt_start_date = DateEntry(
            filter_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.apt_start_date.pack(side="left", padx=(0, 5))
        
        to_label = ModernWidget.create_label(filter_frame, "to")
        to_label.pack(side="left", padx=5)
        
        self.apt_end_date = DateEntry(
            filter_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.apt_end_date.pack(side="left", padx=(5, 20))
        
        # Status filter
        status_label = ModernWidget.create_label(filter_frame, "Status:")
        status_label.pack(side="left", padx=(0, 10))
        
        self.apt_status_filter = ttk.Combobox(
            filter_frame,
            values=["All", "Scheduled", "Completed", "Cancelled"],
            state="readonly",
            width=12
        )
        self.apt_status_filter.set("All")
        self.apt_status_filter.pack(side="left", padx=(0, 20))
        
        generate_btn = ModernWidget.create_button(
            filter_frame, 
            "📊 Generate Report", 
            self.generate_appointment_report, 
            style="primary"
        )
        generate_btn.pack(side="left")
        
        # Report display frame
        self.appointment_report_frame = ModernWidget.create_card(parent, "Appointment Report")
        self.appointment_report_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Initial report
        self.generate_appointment_report()
    
    def create_financial_tab(self, parent):
        """Create financial reports tab"""
        # Filter frame
        filter_frame = ModernWidget.create_frame(parent)
        filter_frame.pack(fill="x", padx=20, pady=20)
        
        # Date range
        date_label = ModernWidget.create_label(filter_frame, "Bill Date Range:")
        date_label.pack(side="left", padx=(0, 10))
        
        self.fin_start_date = DateEntry(
            filter_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.fin_start_date.pack(side="left", padx=(0, 5))
        
        to_label = ModernWidget.create_label(filter_frame, "to")
        to_label.pack(side="left", padx=5)
        
        self.fin_end_date = DateEntry(
            filter_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.fin_end_date.pack(side="left", padx=(5, 20))
        
        generate_btn = ModernWidget.create_button(
            filter_frame, 
            "📊 Generate Report", 
            self.generate_financial_report, 
            style="primary"
        )
        generate_btn.pack(side="left")
        
        # Report display frame
        self.financial_report_frame = ModernWidget.create_card(parent, "Financial Report")
        self.financial_report_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Initial report
        self.generate_financial_report()
    
    def create_lab_tab(self, parent):
        """Create lab reports tab"""
        # Filter frame
        filter_frame = ModernWidget.create_frame(parent)
        filter_frame.pack(fill="x", padx=20, pady=20)
        
        # Date range
        date_label = ModernWidget.create_label(filter_frame, "Test Date Range:")
        date_label.pack(side="left", padx=(0, 10))
        
        self.lab_start_date = DateEntry(
            filter_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.lab_start_date.pack(side="left", padx=(0, 5))
        
        to_label = ModernWidget.create_label(filter_frame, "to")
        to_label.pack(side="left", padx=5)
        
        self.lab_end_date = DateEntry(
            filter_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.lab_end_date.pack(side="left", padx=(5, 20))
        
        # Test type filter
        type_label = ModernWidget.create_label(filter_frame, "Type:")
        type_label.pack(side="left", padx=(0, 10))
        
        self.lab_type_filter = ttk.Combobox(
            filter_frame,
            values=["All", "Blood", "Urine", "X-Ray", "MRI", "CT Scan", "ECG", "Other"],
            state="readonly",
            width=12
        )
        self.lab_type_filter.set("All")
        self.lab_type_filter.pack(side="left", padx=(0, 20))
        
        generate_btn = ModernWidget.create_button(
            filter_frame, 
            "📊 Generate Report", 
            self.generate_lab_report, 
            style="primary"
        )
        generate_btn.pack(side="left")
        
        # Report display frame
        self.lab_report_frame = ModernWidget.create_card(parent, "Lab Test Report")
        self.lab_report_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Initial report
        self.generate_lab_report()
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total patients
        cursor.execute("SELECT COUNT(*) FROM patient")
        stats['total_patients'] = cursor.fetchone()[0]
        
        # This month appointments
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        cursor.execute('''
            SELECT COUNT(*) FROM appointment 
            WHERE appointment_date >= ?
        ''', (start_of_month.strftime('%Y-%m-%d %H:%M:%S'),))
        stats['month_appointments'] = cursor.fetchone()[0]
        
        # Pending bills
        cursor.execute("SELECT COUNT(*) FROM bill WHERE status = 'pending'")
        stats['pending_bills'] = cursor.fetchone()[0]
        
        # Completed tests
        cursor.execute("SELECT COUNT(*) FROM lab_test WHERE status = 'completed'")
        stats['completed_tests'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def create_appointments_chart(self, parent):
        """Create appointments trend chart"""
        # Get data for last 6 months
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Get monthly appointment counts
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', appointment_date) as month,
                COUNT(*) as count
            FROM appointment
            WHERE appointment_date >= date('now', '-6 months')
            GROUP BY strftime('%Y-%m', appointment_date)
            ORDER BY month
        ''')
        
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            no_data_label = ModernWidget.create_label(parent, "No appointment data available", style="secondary")
            no_data_label.pack(expand=True)
            return
        
        # Create chart
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor(ModernStyle.BG_SECONDARY)
        ax.set_facecolor(ModernStyle.BG_SECONDARY)
        
        months = [item[0] for item in data]
        counts = [item[1] for item in data]
        
        ax.plot(months, counts, marker='o', linewidth=2, markersize=6, color=ModernStyle.BTN_PRIMARY)
        ax.set_title('Monthly Appointments', color=ModernStyle.TEXT_PRIMARY, fontsize=12)
        ax.set_xlabel('Month', color=ModernStyle.TEXT_PRIMARY)
        ax.set_ylabel('Count', color=ModernStyle.TEXT_PRIMARY)
        
        # Style the chart
        ax.tick_params(colors=ModernStyle.TEXT_PRIMARY)
        ax.spines['bottom'].set_color(ModernStyle.TEXT_PRIMARY)
        ax.spines['left'].set_color(ModernStyle.TEXT_PRIMARY)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Embed chart
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
    
    def create_revenue_chart(self, parent):
        """Create revenue trend chart"""
        # Get data for last 6 months
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Get monthly revenue
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', bill_date) as month,
                SUM(paid_amount) as revenue
            FROM bill
            WHERE bill_date >= date('now', '-6 months')
            GROUP BY strftime('%Y-%m', bill_date)
            ORDER BY month
        ''')
        
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            no_data_label = ModernWidget.create_label(parent, "No revenue data available", style="secondary")
            no_data_label.pack(expand=True)
            return
        
        # Create chart
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor(ModernStyle.BG_SECONDARY)
        ax.set_facecolor(ModernStyle.BG_SECONDARY)
        
        months = [item[0] for item in data]
        revenue = [item[1] or 0 for item in data]
        
        ax.bar(months, revenue, color=ModernStyle.BG_SUCCESS, alpha=0.8)
        ax.set_title('Monthly Revenue', color=ModernStyle.TEXT_PRIMARY, fontsize=12)
        ax.set_xlabel('Month', color=ModernStyle.TEXT_PRIMARY)
        ax.set_ylabel('Revenue ($)', color=ModernStyle.TEXT_PRIMARY)
        
        # Style the chart
        ax.tick_params(colors=ModernStyle.TEXT_PRIMARY)
        ax.spines['bottom'].set_color(ModernStyle.TEXT_PRIMARY)
        ax.spines['left'].set_color(ModernStyle.TEXT_PRIMARY)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Embed chart
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
    
    def generate_patient_report(self):
        """Generate patient report"""
        # Clear existing content
        for widget in self.patient_report_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                for child in widget.winfo_children()[1:]:  # Keep title
                    child.destroy()
        
        start_date = self.patient_start_date.get_date()
        end_date = self.patient_end_date.get_date()
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Get patient statistics
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN gender = 'male' THEN 1 END) as male,
                COUNT(CASE WHEN gender = 'female' THEN 1 END) as female,
                AVG(CASE 
                    WHEN date_of_birth IS NOT NULL 
                    THEN (julianday('now') - julianday(date_of_birth)) / 365.25 
                END) as avg_age
            FROM patient
            WHERE DATE(created_at) BETWEEN ? AND ?
        ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        
        stats = cursor.fetchone()
        
        # Get age distribution
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN (julianday('now') - julianday(date_of_birth)) / 365.25 < 18 THEN 'Under 18'
                    WHEN (julianday('now') - julianday(date_of_birth)) / 365.25 < 35 THEN '18-34'
                    WHEN (julianday('now') - julianday(date_of_birth)) / 365.25 < 55 THEN '35-54'
                    ELSE '55+'
                END as age_group,
                COUNT(*) as count
            FROM patient
            WHERE DATE(created_at) BETWEEN ? AND ?
            GROUP BY age_group
        ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        
        age_data = cursor.fetchall()
        conn.close()
        
        # Create report content
        content_frame = ModernWidget.create_frame(self.patient_report_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Summary statistics
        summary_frame = ModernWidget.create_frame(content_frame)
        summary_frame.pack(fill="x", pady=(0, 20))
        
        total_label = ModernWidget.create_label(
            summary_frame, 
            f"Total Patients: {stats[0]}", 
            size="large"
        )
        total_label.pack(anchor="w")
        
        gender_label = ModernWidget.create_label(
            summary_frame, 
            f"Male: {stats[1]} | Female: {stats[2]}", 
            style="secondary"
        )
        gender_label.pack(anchor="w")
        
        if stats[3]:
            age_label = ModernWidget.create_label(
                summary_frame, 
                f"Average Age: {stats[3]:.1f} years", 
                style="secondary"
            )
            age_label.pack(anchor="w")
        
        # Age distribution chart
        if age_data:
            chart_frame = ModernWidget.create_frame(content_frame)
            chart_frame.pack(fill="both", expand=True)
            
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor(ModernStyle.BG_SECONDARY)
            ax.set_facecolor(ModernStyle.BG_SECONDARY)
            
            age_groups = [item[0] for item in age_data]
            counts = [item[1] for item in age_data]
            
            ax.pie(counts, labels=age_groups, autopct='%1.1f%%', startangle=90)
            ax.set_title('Age Distribution', color=ModernStyle.TEXT_PRIMARY, fontsize=12)
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def generate_appointment_report(self):
        """Generate appointment report"""
        # Clear existing content
        for widget in self.appointment_report_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                for child in widget.winfo_children()[1:]:  # Keep title
                    child.destroy()
        
        start_date = self.apt_start_date.get_date()
        end_date = self.apt_end_date.get_date()
        status_filter = self.apt_status_filter.get().lower()
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Build query based on filters
        query = '''
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'scheduled' THEN 1 END) as scheduled,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled
            FROM appointment
            WHERE DATE(appointment_date) BETWEEN ? AND ?
        '''
        
        params = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]
        
        if status_filter != 'all':
            query += ' AND status = ?'
            params.append(status_filter)
        
        cursor.execute(query, params)
        stats = cursor.fetchone()
        
        # Get appointment types
        type_query = '''
            SELECT appointment_type, COUNT(*) as count
            FROM appointment
            WHERE DATE(appointment_date) BETWEEN ? AND ?
        '''
        
        type_params = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]
        
        if status_filter != 'all':
            type_query += ' AND status = ?'
            type_params.append(status_filter)
        
        type_query += ' GROUP BY appointment_type ORDER BY count DESC'
        
        cursor.execute(type_query, type_params)
        type_data = cursor.fetchall()
        
        conn.close()
        
        # Create report content
        content_frame = ModernWidget.create_frame(self.appointment_report_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Summary statistics
        summary_frame = ModernWidget.create_frame(content_frame)
        summary_frame.pack(fill="x", pady=(0, 20))
        
        total_label = ModernWidget.create_label(
            summary_frame, 
            f"Total Appointments: {stats[0]}", 
            size="large"
        )
        total_label.pack(anchor="w")
        
        status_label = ModernWidget.create_label(
            summary_frame, 
            f"Scheduled: {stats[1]} | Completed: {stats[2]} | Cancelled: {stats[3]}", 
            style="secondary"
        )
        status_label.pack(anchor="w")
        
        # Appointment types chart
        if type_data:
            chart_frame = ModernWidget.create_frame(content_frame)
            chart_frame.pack(fill="both", expand=True)
            
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor(ModernStyle.BG_SECONDARY)
            ax.set_facecolor(ModernStyle.BG_SECONDARY)
            
            types = [item[0] for item in type_data]
            counts = [item[1] for item in type_data]
            
            ax.bar(types, counts, color=ModernStyle.BTN_PRIMARY, alpha=0.8)
            ax.set_title('Appointment Types', color=ModernStyle.TEXT_PRIMARY, fontsize=12)
            ax.set_xlabel('Type', color=ModernStyle.TEXT_PRIMARY)
            ax.set_ylabel('Count', color=ModernStyle.TEXT_PRIMARY)
            
            # Style the chart
            ax.tick_params(colors=ModernStyle.TEXT_PRIMARY)
            ax.spines['bottom'].set_color(ModernStyle.TEXT_PRIMARY)
            ax.spines['left'].set_color(ModernStyle.TEXT_PRIMARY)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def generate_financial_report(self):
        """Generate financial report"""
        # Clear existing content
        for widget in self.financial_report_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                for child in widget.winfo_children()[1:]:  # Keep title
                    child.destroy()
        
        start_date = self.fin_start_date.get_date()
        end_date = self.fin_end_date.get_date()
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Get financial statistics
        cursor.execute('''
            SELECT 
                COUNT(*) as total_bills,
                SUM(total_amount) as total_billed,
                SUM(paid_amount) as total_paid,
                SUM(total_amount - paid_amount) as outstanding,
                COUNT(CASE WHEN status = 'paid' THEN 1 END) as paid_bills,
                COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_bills,
                COUNT(CASE WHEN status = 'overdue' THEN 1 END) as overdue_bills
            FROM bill
            WHERE DATE(bill_date) BETWEEN ? AND ?
        ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        
        stats = cursor.fetchone()
        
        # Get daily revenue
        cursor.execute('''
            SELECT 
                DATE(bill_date) as date,
                SUM(paid_amount) as daily_revenue
            FROM bill
            WHERE DATE(bill_date) BETWEEN ? AND ?
            GROUP BY DATE(bill_date)
            ORDER BY date
        ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        
        daily_data = cursor.fetchall()
        conn.close()
        
        # Create report content
        content_frame = ModernWidget.create_frame(self.financial_report_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Summary statistics
        summary_frame = ModernWidget.create_frame(content_frame)
        summary_frame.pack(fill="x", pady=(0, 20))
        
        total_label = ModernWidget.create_label(
            summary_frame, 
            f"Total Bills: {stats[0]}", 
            size="large"
        )
        total_label.pack(anchor="w")
        
        revenue_label = ModernWidget.create_label(
            summary_frame, 
            f"Total Billed: ${stats[1] or 0:.2f} | Total Paid: ${stats[2] or 0:.2f}", 
            style="secondary"
        )
        revenue_label.pack(anchor="w")
        
        outstanding_label = ModernWidget.create_label(
            summary_frame, 
            f"Outstanding: ${stats[3] or 0:.2f}", 
            style="warning"
        )
        outstanding_label.pack(anchor="w")
        
        status_label = ModernWidget.create_label(
            summary_frame, 
            f"Paid: {stats[4]} | Pending: {stats[5]} | Overdue: {stats[6]}", 
            style="secondary"
        )
        status_label.pack(anchor="w")
        
        # Daily revenue chart
        if daily_data:
            chart_frame = ModernWidget.create_frame(content_frame)
            chart_frame.pack(fill="both", expand=True)
            
            fig, ax = plt.subplots(figsize=(10, 4))
            fig.patch.set_facecolor(ModernStyle.BG_SECONDARY)
            ax.set_facecolor(ModernStyle.BG_SECONDARY)
            
            dates = [item[0] for item in daily_data]
            revenue = [item[1] or 0 for item in daily_data]
            
            ax.plot(dates, revenue, marker='o', linewidth=2, markersize=4, color=ModernStyle.BG_SUCCESS)
            ax.set_title('Daily Revenue', color=ModernStyle.TEXT_PRIMARY, fontsize=12)
            ax.set_xlabel('Date', color=ModernStyle.TEXT_PRIMARY)
            ax.set_ylabel('Revenue ($)', color=ModernStyle.TEXT_PRIMARY)
            
            # Style the chart
            ax.tick_params(colors=ModernStyle.TEXT_PRIMARY)
            ax.spines['bottom'].set_color(ModernStyle.TEXT_PRIMARY)
            ax.spines['left'].set_color(ModernStyle.TEXT_PRIMARY)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def generate_lab_report(self):
        """Generate lab test report"""
        # Clear existing content
        for widget in self.lab_report_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                for child in widget.winfo_children()[1:]:  # Keep title
                    child.destroy()
        
        start_date = self.lab_start_date.get_date()
        end_date = self.lab_end_date.get_date()
        type_filter = self.lab_type_filter.get().lower()
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Build query based on filters
        query = '''
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'ordered' THEN 1 END) as ordered,
                COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed
            FROM lab_test
            WHERE DATE(ordered_date) BETWEEN ? AND ?
        '''
        
        params = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]
        
        if type_filter != 'all':
            query += ' AND test_type = ?'
            params.append(type_filter)
        
        cursor.execute(query, params)
        stats = cursor.fetchone()
        
        # Get test types distribution
        type_query = '''
            SELECT test_type, COUNT(*) as count
            FROM lab_test
            WHERE DATE(ordered_date) BETWEEN ? AND ?
        '''
        
        type_params = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]
        
        if type_filter != 'all':
            type_query += ' AND test_type = ?'
            type_params.append(type_filter)
        
        type_query += ' GROUP BY test_type ORDER BY count DESC'
        
        cursor.execute(type_query, type_params)
        type_data = cursor.fetchall()
        
        conn.close()
        
        # Create report content
        content_frame = ModernWidget.create_frame(self.lab_report_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Summary statistics
        summary_frame = ModernWidget.create_frame(content_frame)
        summary_frame.pack(fill="x", pady=(0, 20))
        
        total_label = ModernWidget.create_label(
            summary_frame, 
            f"Total Tests: {stats[0]}", 
            size="large"
        )
        total_label.pack(anchor="w")
        
        status_label = ModernWidget.create_label(
            summary_frame, 
            f"Ordered: {stats[1]} | In Progress: {stats[2]} | Completed: {stats[3]}", 
            style="secondary"
        )
        status_label.pack(anchor="w")
        
        # Test types chart
        if type_data:
            chart_frame = ModernWidget.create_frame(content_frame)
            chart_frame.pack(fill="both", expand=True)
            
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor(ModernStyle.BG_SECONDARY)
            ax.set_facecolor(ModernStyle.BG_SECONDARY)
            
            types = [item[0].title() for item in type_data]
            counts = [item[1] for item in type_data]
            
            ax.pie(counts, labels=types, autopct='%1.1f%%', startangle=90)
            ax.set_title('Test Types Distribution', color=ModernStyle.TEXT_PRIMARY, fontsize=12)
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def export_report(self):
        """Export current report to file"""
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        
        # Get filename from user
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title=f"Export {current_tab} Report"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(f"Hospital Management System - {current_tab}\n")
                    f.write("=" * 50 + "\n")
                    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    # Add report-specific content based on current tab
                    if "Dashboard" in current_tab:
                        stats = self.get_dashboard_stats()
                        f.write(f"Total Patients: {stats['total_patients']}\n")
                        f.write(f"This Month Appointments: {stats['month_appointments']}\n")
                        f.write(f"Pending Bills: {stats['pending_bills']}\n")
                        f.write(f"Completed Tests: {stats['completed_tests']}\n")
                    
                    # Add more export logic for other tabs as needed
                
                messagebox.showinfo("Success", f"Report exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {str(e)}")