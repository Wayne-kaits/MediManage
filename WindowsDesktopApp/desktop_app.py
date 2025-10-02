#!/usr/bin/env python3
"""
Hospital Management System - Advanced Windows Desktop Application
Modern UI with Bootstrap-inspired dark theme
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import json
import hashlib
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from tkcalendar import DateEntry
import threading
import webbrowser

# Add parent directory to path to import models
sys.path.append(str(Path(__file__).parent.parent))

class ModernStyle:
    """Modern dark theme styling constants"""
    
    # Colors (Bootstrap dark theme inspired)
    BG_PRIMARY = "#212529"      # Dark background
    BG_SECONDARY = "#343a40"    # Secondary background
    BG_SUCCESS = "#198754"      # Success green
    BG_DANGER = "#dc3545"       # Danger red
    BG_WARNING = "#ffc107"      # Warning yellow
    BG_INFO = "#0dcaf0"         # Info cyan
    BG_LIGHT = "#f8f9fa"        # Light background
    BG_DARK = "#343a40"         # Dark background
    
    # Text colors
    TEXT_PRIMARY = "#ffffff"    # Primary text
    TEXT_SECONDARY = "#6c757d"  # Secondary text
    TEXT_MUTED = "#6c757d"      # Muted text
    TEXT_DARK = "#212529"       # Dark text
    
    # Border colors
    BORDER_COLOR = "#495057"    # Border color
    BORDER_LIGHT = "#dee2e6"    # Light border
    
    # Button colors
    BTN_PRIMARY = "#0d6efd"     # Primary button
    BTN_SUCCESS = "#198754"     # Success button
    BTN_DANGER = "#dc3545"      # Danger button
    BTN_WARNING = "#ffc107"     # Warning button
    BTN_INFO = "#0dcaf0"        # Info button
    BTN_SECONDARY = "#6c757d"   # Secondary button
    
    # Fonts
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_SMALL = 9
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_LARGE = 12
    FONT_SIZE_XLARGE = 14
    FONT_SIZE_TITLE = 16

class DatabaseManager:
    """Database operations manager"""
    
    def __init__(self):
        self.db_path = Path(__file__).parent.parent / "data" / "hospital.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(str(self.db_path))
    
    def init_database(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'staff',
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth DATE NOT NULL,
                gender TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                emergency_contact TEXT,
                emergency_phone TEXT,
                blood_type TEXT,
                allergies TEXT,
                medical_history TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                appointment_date TIMESTAMP NOT NULL,
                appointment_type TEXT NOT NULL,
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patient (id),
                FOREIGN KEY (doctor_id) REFERENCES user (id)
            )
        ''')
        
        # Bills table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bill (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_number TEXT UNIQUE NOT NULL,
                patient_id INTEGER NOT NULL,
                appointment_id INTEGER,
                total_amount REAL NOT NULL,
                paid_amount REAL DEFAULT 0.0,
                status TEXT DEFAULT 'pending',
                bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patient (id),
                FOREIGN KEY (appointment_id) REFERENCES appointment (id)
            )
        ''')
        
        # Bill items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bill_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (bill_id) REFERENCES bill (id)
            )
        ''')
        
        # Lab tests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lab_test (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id TEXT UNIQUE NOT NULL,
                patient_id INTEGER NOT NULL,
                test_name TEXT NOT NULL,
                test_type TEXT NOT NULL,
                ordered_by INTEGER NOT NULL,
                status TEXT DEFAULT 'ordered',
                results TEXT,
                normal_range TEXT,
                notes TEXT,
                ordered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_date TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patient (id),
                FOREIGN KEY (ordered_by) REFERENCES user (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Create default admin user
        self.create_default_admin()
    
    def create_default_admin(self):
        """Create default admin user if not exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM user WHERE username = 'admin'")
        if not cursor.fetchone():
            password_hash = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute('''
                INSERT INTO user (username, email, password_hash, role, first_name, last_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('admin', 'admin@hospital.com', password_hash, 'admin', 'System', 'Administrator'))
            conn.commit()
        
        conn.close()

class ModernWidget:
    """Custom modern widgets with dark theme styling"""
    
    @staticmethod
    def create_button(parent, text, command=None, style="primary", width=None):
        """Create a modern styled button"""
        colors = {
            "primary": (ModernStyle.BTN_PRIMARY, ModernStyle.TEXT_PRIMARY),
            "success": (ModernStyle.BTN_SUCCESS, ModernStyle.TEXT_PRIMARY),
            "danger": (ModernStyle.BTN_DANGER, ModernStyle.TEXT_PRIMARY),
            "warning": (ModernStyle.BTN_WARNING, ModernStyle.TEXT_DARK),
            "info": (ModernStyle.BTN_INFO, ModernStyle.TEXT_DARK),
            "secondary": (ModernStyle.BTN_SECONDARY, ModernStyle.TEXT_PRIMARY)
        }
        
        bg_color, fg_color = colors.get(style, colors["primary"])
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL, "bold"),
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        
        if width:
            btn.config(width=width)
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=ModernWidget.lighten_color(bg_color))
        
        def on_leave(e):
            btn.config(bg=bg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    @staticmethod
    def create_entry(parent, placeholder="", width=None):
        """Create a modern styled entry widget"""
        entry = tk.Entry(
            parent,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_PRIMARY,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightcolor=ModernStyle.BTN_PRIMARY,
            highlightbackground=ModernStyle.BORDER_COLOR,
            insertbackground=ModernStyle.TEXT_PRIMARY
        )
        
        if width:
            entry.config(width=width)
        
        # Placeholder functionality
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=ModernStyle.TEXT_SECONDARY)
            
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=ModernStyle.TEXT_PRIMARY)
            
            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg=ModernStyle.TEXT_SECONDARY)
            
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
        
        return entry
    
    @staticmethod
    def create_text(parent, height=10, width=None):
        """Create a modern styled text widget"""
        text = tk.Text(
            parent,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_PRIMARY,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightcolor=ModernStyle.BTN_PRIMARY,
            highlightbackground=ModernStyle.BORDER_COLOR,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            height=height,
            wrap=tk.WORD
        )
        
        if width:
            text.config(width=width)
        
        return text
    
    @staticmethod
    def create_label(parent, text, style="primary", size="normal"):
        """Create a modern styled label"""
        colors = {
            "primary": ModernStyle.TEXT_PRIMARY,
            "secondary": ModernStyle.TEXT_SECONDARY,
            "success": ModernStyle.BG_SUCCESS,
            "danger": ModernStyle.BG_DANGER,
            "warning": ModernStyle.BG_WARNING,
            "info": ModernStyle.BG_INFO
        }
        
        sizes = {
            "small": ModernStyle.FONT_SIZE_SMALL,
            "normal": ModernStyle.FONT_SIZE_NORMAL,
            "large": ModernStyle.FONT_SIZE_LARGE,
            "xlarge": ModernStyle.FONT_SIZE_XLARGE,
            "title": ModernStyle.FONT_SIZE_TITLE
        }
        
        label = tk.Label(
            parent,
            text=text,
            bg=ModernStyle.BG_PRIMARY,
            fg=colors.get(style, colors["primary"]),
            font=(ModernStyle.FONT_FAMILY, sizes.get(size, sizes["normal"]))
        )
        
        return label
    
    @staticmethod
    def create_frame(parent, bg_color=None):
        """Create a modern styled frame"""
        frame = tk.Frame(
            parent,
            bg=bg_color or ModernStyle.BG_PRIMARY,
            relief="flat",
            borderwidth=0
        )
        return frame
    
    @staticmethod
    def create_card(parent, title="", padding=20):
        """Create a card-like container"""
        card = tk.Frame(
            parent,
            bg=ModernStyle.BG_SECONDARY,
            relief="flat",
            borderwidth=1,
            highlightbackground=ModernStyle.BORDER_COLOR,
            highlightthickness=1
        )
        
        if title:
            title_label = ModernWidget.create_label(card, title, size="large")
            title_label.pack(anchor="w", padx=padding, pady=(padding, 10))
        
        return card
    
    @staticmethod
    def lighten_color(color, factor=0.1):
        """Lighten a hex color"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

class LoginWindow:
    """Modern login window"""
    
    def __init__(self, app):
        self.app = app
        self.window = tk.Toplevel()
        self.window.title("Hospital Management System - Login")
        self.window.geometry("400x500")
        self.window.configure(bg=ModernStyle.BG_PRIMARY)
        self.window.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Make it modal
        self.window.transient(app.root)
        self.window.grab_set()
        
        self.create_widgets()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"400x500+{x}+{y}")
    
    def create_widgets(self):
        """Create login form widgets"""
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Logo/Title
        title_label = ModernWidget.create_label(
            main_frame, 
            "🏥 Hospital Management", 
            size="title"
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ModernWidget.create_label(
            main_frame, 
            "Desktop Application", 
            style="secondary",
            size="normal"
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Login form card
        login_card = ModernWidget.create_card(main_frame, "Sign In")
        login_card.pack(fill="x", pady=20)
        
        # Form container
        form_frame = ModernWidget.create_frame(login_card)
        form_frame.pack(fill="x", padx=20, pady=20)
        
        # Username field
        username_label = ModernWidget.create_label(form_frame, "Username")
        username_label.pack(anchor="w", pady=(0, 5))
        
        self.username_entry = ModernWidget.create_entry(form_frame, width=30)
        self.username_entry.pack(fill="x", pady=(0, 15))
        self.username_entry.focus()
        
        # Password field
        password_label = ModernWidget.create_label(form_frame, "Password")
        password_label.pack(anchor="w", pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            show="*",
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_PRIMARY,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightcolor=ModernStyle.BTN_PRIMARY,
            highlightbackground=ModernStyle.BORDER_COLOR,
            insertbackground=ModernStyle.TEXT_PRIMARY
        )
        self.password_entry.pack(fill="x", pady=(0, 20))
        
        # Login button
        login_btn = ModernWidget.create_button(
            form_frame, 
            "Sign In", 
            self.login,
            style="primary"
        )
        login_btn.pack(fill="x", pady=(0, 10))
        
        # Default credentials info
        info_frame = ModernWidget.create_frame(main_frame)
        info_frame.pack(fill="x", pady=20)
        
        info_label = ModernWidget.create_label(
            info_frame, 
            "Default Credentials:", 
            style="secondary",
            size="small"
        )
        info_label.pack()
        
        cred_label = ModernWidget.create_label(
            info_frame, 
            "Username: admin | Password: admin123", 
            style="info",
            size="small"
        )
        cred_label.pack(pady=5)
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Verify credentials
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            SELECT id, username, role, first_name, last_name 
            FROM user 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.app.current_user = {
                'id': user[0],
                'username': user[1],
                'role': user[2],
                'first_name': user[3],
                'last_name': user[4]
            }
            self.window.destroy()
            self.app.show_main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password")

class HospitalManagementApp:
    """Main Hospital Management Desktop Application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window initially
        self.current_user = None
        self.db = DatabaseManager()
        
        # Configure root window
        self.root.title("Hospital Management System")
        self.root.geometry("1400x900")
        self.root.configure(bg=ModernStyle.BG_PRIMARY)
        self.root.state('zoomed')  # Maximize window
        
        # Show login window
        self.show_login()
    
    def show_login(self):
        """Show login window"""
        LoginWindow(self)
    
    def show_main_window(self):
        """Show main application window"""
        self.root.deiconify()
        self.create_main_interface()
    
    def create_main_interface(self):
        """Create the main application interface"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main layout
        self.create_header()
        self.create_sidebar()
        self.create_main_content()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_header(self):
        """Create application header"""
        header_frame = ModernWidget.create_frame(self.root, ModernStyle.BG_DARK)
        header_frame.pack(fill="x", side="top")
        
        # Left side - Logo and title
        left_frame = ModernWidget.create_frame(header_frame, ModernStyle.BG_DARK)
        left_frame.pack(side="left", padx=20, pady=10)
        
        title_label = ModernWidget.create_label(
            left_frame, 
            "🏥 Hospital Management System", 
            size="large"
        )
        title_label.pack(side="left")
        
        # Right side - User info and logout
        right_frame = ModernWidget.create_frame(header_frame, ModernStyle.BG_DARK)
        right_frame.pack(side="right", padx=20, pady=10)
        
        user_label = ModernWidget.create_label(
            right_frame, 
            f"Welcome, {self.current_user['first_name']} {self.current_user['last_name']} ({self.current_user['role'].title()})",
            style="secondary"
        )
        user_label.pack(side="left", padx=(0, 20))
        
        logout_btn = ModernWidget.create_button(
            right_frame, 
            "Logout", 
            self.logout,
            style="danger"
        )
        logout_btn.pack(side="right")
    
    def create_sidebar(self):
        """Create navigation sidebar"""
        self.sidebar_frame = ModernWidget.create_frame(self.root, ModernStyle.BG_SECONDARY)
        self.sidebar_frame.pack(fill="y", side="left")
        
        # Navigation buttons
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("👥 Patients", self.show_patients),
            ("📅 Appointments", self.show_appointments),
            ("💰 Billing", self.show_billing),
            ("🧪 Lab Tests", self.show_lab_tests),
            ("📈 Reports", self.show_reports),
        ]
        
        if self.current_user['role'] == 'admin':
            nav_buttons.append(("👤 User Management", self.show_user_management))
        
        for text, command in nav_buttons:
            btn = tk.Button(
                self.sidebar_frame,
                text=text,
                command=command,
                bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.TEXT_PRIMARY,
                font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
                relief="flat",
                borderwidth=0,
                padx=20,
                pady=15,
                anchor="w",
                width=20,
                cursor="hand2"
            )
            btn.pack(fill="x", padx=5, pady=2)
            
            # Hover effects
            def on_enter(e, button=btn):
                button.config(bg=ModernStyle.BTN_PRIMARY)
            
            def on_leave(e, button=btn):
                button.config(bg=ModernStyle.BG_SECONDARY)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def create_main_content(self):
        """Create main content area"""
        self.main_frame = ModernWidget.create_frame(self.root)
        self.main_frame.pack(fill="both", expand=True, side="right")
    
    def clear_main_content(self):
        """Clear main content area"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show dashboard"""
        self.clear_main_content()
        
        # Dashboard title
        title_frame = ModernWidget.create_frame(self.main_frame)
        title_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ModernWidget.create_label(title_frame, "Dashboard", size="title")
        title_label.pack(anchor="w")
        
        # Statistics cards
        stats_frame = ModernWidget.create_frame(self.main_frame)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Get statistics from database
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Total patients
        cursor.execute("SELECT COUNT(*) FROM patient")
        total_patients = cursor.fetchone()[0]
        
        # Today's appointments
        today = datetime.now().date()
        cursor.execute("SELECT COUNT(*) FROM appointment WHERE DATE(appointment_date) = ?", (today,))
        today_appointments = cursor.fetchone()[0]
        
        # Pending bills
        cursor.execute("SELECT COUNT(*) FROM bill WHERE status = 'pending'")
        pending_bills = cursor.fetchone()[0]
        
        # Pending lab tests
        cursor.execute("SELECT COUNT(*) FROM lab_test WHERE status = 'ordered'")
        pending_tests = cursor.fetchone()[0]
        
        conn.close()
        
        # Create stat cards
        stats = [
            ("Total Patients", total_patients, ModernStyle.BTN_PRIMARY),
            ("Today's Appointments", today_appointments, ModernStyle.BG_SUCCESS),
            ("Pending Bills", pending_bills, ModernStyle.BG_WARNING),
            ("Pending Tests", pending_tests, ModernStyle.BG_INFO)
        ]
        
        for i, (title, value, color) in enumerate(stats):
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
        
        # Recent activities section
        activities_frame = ModernWidget.create_frame(self.main_frame)
        activities_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Recent patients
        recent_frame = ModernWidget.create_card(activities_frame, "Recent Activities")
        recent_frame.pack(fill="both", expand=True)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(recent_frame)
        notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Recent patients tab
        patients_tab = ModernWidget.create_frame(notebook)
        notebook.add(patients_tab, text="Recent Patients")
        
        # Recent appointments tab
        appointments_tab = ModernWidget.create_frame(notebook)
        notebook.add(appointments_tab, text="Recent Appointments")
        
        # Populate recent patients
        self.populate_recent_patients(patients_tab)
        self.populate_recent_appointments(appointments_tab)
    
    def populate_recent_patients(self, parent):
        """Populate recent patients list"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT patient_id, first_name, last_name, date_of_birth, phone, created_at
            FROM patient 
            ORDER BY created_at DESC 
            LIMIT 10
        ''')
        
        patients = cursor.fetchall()
        conn.close()
        
        if not patients:
            no_data_label = ModernWidget.create_label(parent, "No patients found", style="secondary")
            no_data_label.pack(pady=20)
            return
        
        # Create treeview for patients
        columns = ("ID", "Name", "Age", "Phone", "Added")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for patient in patients:
            patient_id, first_name, last_name, dob, phone, created_at = patient
            age = self.calculate_age(dob)
            name = f"{first_name} {last_name}"
            created_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            
            tree.insert("", "end", values=(patient_id, name, age, phone or "N/A", created_date))
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    def populate_recent_appointments(self, parent):
        """Populate recent appointments list"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.appointment_date, a.appointment_type, a.status,
                   p.first_name, p.last_name, p.patient_id,
                   u.first_name, u.last_name
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN user u ON a.doctor_id = u.id
            ORDER BY a.created_at DESC 
            LIMIT 10
        ''')
        
        appointments = cursor.fetchall()
        conn.close()
        
        if not appointments:
            no_data_label = ModernWidget.create_label(parent, "No appointments found", style="secondary")
            no_data_label.pack(pady=20)
            return
        
        # Create treeview for appointments
        columns = ("Date", "Patient", "Doctor", "Type", "Status")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for appointment in appointments:
            date, apt_type, status, p_fname, p_lname, p_id, d_fname, d_lname = appointment
            apt_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
            patient_name = f"{p_fname} {p_lname}"
            doctor_name = f"Dr. {d_fname} {d_lname}"
            
            tree.insert("", "end", values=(apt_date, patient_name, doctor_name, apt_type, status.title()))
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    def calculate_age(self, birth_date):
        """Calculate age from birth date"""
        if isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        
        today = datetime.now().date()
        age = today.year - birth_date.year
        
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        
        return age
    
    def show_patients(self):
        """Show patients management"""
        from patient_management import PatientManagement
        self.clear_main_content()
        PatientManagement(self.main_frame, self.db, self.current_user)
    
    def show_appointments(self):
        """Show appointments management"""
        from appointment_management import AppointmentManagement
        self.clear_main_content()
        AppointmentManagement(self.main_frame, self.db, self.current_user)
    
    def show_billing(self):
        """Show billing management"""
        from billing_management import BillingManagement
        self.clear_main_content()
        BillingManagement(self.main_frame, self.db, self.current_user)
    
    def show_lab_tests(self):
        """Show lab tests management"""
        from lab_management import LabManagement
        self.clear_main_content()
        LabManagement(self.main_frame, self.db, self.current_user)
    
    def show_reports(self):
        """Show reports"""
        from reports_management import ReportsManagement
        self.clear_main_content()
        ReportsManagement(self.main_frame, self.db, self.current_user)
    
    def show_user_management(self):
        """Show user management (admin only)"""
        from user_management import UserManagement
        self.clear_main_content()
        UserManagement(self.main_frame, self.db, self.current_user)
    
    def logout(self):
        """Logout user"""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.current_user = None
            self.root.withdraw()
            self.show_login()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = HospitalManagementApp()
    app.run()