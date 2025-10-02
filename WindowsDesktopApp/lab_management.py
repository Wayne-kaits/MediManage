"""
Lab Management Module
Advanced lab test management with modern UI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import sqlite3
from desktop_app import ModernWidget, ModernStyle

class LabManagement:
    """Lab management interface"""
    
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        self.tests_data = []
        self.selected_test = None
        
        self.create_interface()
        self.load_tests()
    
    def create_interface(self):
        """Create lab management interface"""
        # Title
        title_frame = ModernWidget.create_frame(self.parent)
        title_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ModernWidget.create_label(title_frame, "Lab Test Management", size="title")
        title_label.pack(side="left")
        
        # Action buttons
        btn_frame = ModernWidget.create_frame(title_frame)
        btn_frame.pack(side="right")
        
        order_btn = ModernWidget.create_button(btn_frame, "➕ Order Test", self.order_test, style="success")
        order_btn.pack(side="left", padx=(0, 10))
        
        edit_btn = ModernWidget.create_button(btn_frame, "✏️ Edit", self.edit_test, style="primary")
        edit_btn.pack(side="left", padx=(0, 10))
        
        results_btn = ModernWidget.create_button(btn_frame, "📋 Add Results", self.add_results, style="info")
        results_btn.pack(side="left", padx=(0, 10))
        
        complete_btn = ModernWidget.create_button(btn_frame, "✅ Complete", self.complete_test, style="success")
        complete_btn.pack(side="left", padx=(0, 10))
        
        view_btn = ModernWidget.create_button(btn_frame, "👁️ View Details", self.view_test, style="info")
        view_btn.pack(side="left")
        
        # Filter frame
        filter_frame = ModernWidget.create_frame(self.parent)
        filter_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Status filter
        status_label = ModernWidget.create_label(filter_frame, "Status:")
        status_label.pack(side="left", padx=(0, 10))
        
        self.status_filter = ttk.Combobox(
            filter_frame,
            values=["All", "Ordered", "In Progress", "Completed"],
            state="readonly",
            width=12
        )
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=(0, 20))
        self.status_filter.bind("<<ComboboxSelected>>", self.on_status_filter)
        
        # Test type filter
        type_label = ModernWidget.create_label(filter_frame, "Type:")
        type_label.pack(side="left", padx=(0, 10))
        
        self.type_filter = ttk.Combobox(
            filter_frame,
            values=["All", "Blood", "Urine", "X-Ray", "MRI", "CT Scan", "ECG", "Other"],
            state="readonly",
            width=12
        )
        self.type_filter.set("All")
        self.type_filter.pack(side="left", padx=(0, 20))
        self.type_filter.bind("<<ComboboxSelected>>", self.on_type_filter)
        
        # Date filter
        date_label = ModernWidget.create_label(filter_frame, "Date:")
        date_label.pack(side="left", padx=(0, 10))
        
        self.date_filter = DateEntry(
            filter_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.date_filter.pack(side="left", padx=(0, 20))
        self.date_filter.bind("<<DateEntrySelected>>", self.on_date_filter)
        
        # Search
        search_label = ModernWidget.create_label(filter_frame, "Search:")
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        search_entry = ModernWidget.create_entry(filter_frame, "Enter test ID or patient name...", width=30)
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.config(textvariable=self.search_var)
        
        refresh_btn = ModernWidget.create_button(filter_frame, "🔄 Refresh", self.load_tests, style="secondary")
        refresh_btn.pack(side="left")
        
        # Tests list
        list_frame = ModernWidget.create_card(self.parent, "Lab Tests List")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create treeview
        self.create_tests_tree(list_frame)
    
    def create_tests_tree(self, parent):
        """Create lab tests treeview"""
        tree_frame = ModernWidget.create_frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Columns
        columns = ("ID", "Test ID", "Patient", "Test Name", "Type", "Ordered By", "Status", "Ordered Date", "Completed Date")
        self.tests_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        column_widths = {"ID": 50, "Test ID": 100, "Patient": 150, "Test Name": 150, "Type": 100,
                        "Ordered By": 120, "Status": 100, "Ordered Date": 100, "Completed Date": 100}
        
        for col in columns:
            self.tests_tree.heading(col, text=col, command=lambda c=col: self.sort_tests(c))
            self.tests_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tests_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tests_tree.xview)
        
        self.tests_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tests_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Bind selection event
        self.tests_tree.bind("<<TreeviewSelect>>", self.on_test_select)
        self.tests_tree.bind("<Double-1>", lambda e: self.view_test())
    
    def load_tests(self):
        """Load lab tests from database"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT lt.id, lt.test_id, lt.test_name, lt.test_type, lt.status, 
                   lt.ordered_date, lt.completed_date, lt.results, lt.normal_range, lt.notes,
                   p.first_name, p.last_name, p.patient_id,
                   u.first_name, u.last_name
            FROM lab_test lt
            JOIN patient p ON lt.patient_id = p.id
            JOIN user u ON lt.ordered_by = u.id
            ORDER BY lt.ordered_date DESC
        ''')
        
        self.tests_data = cursor.fetchall()
        conn.close()
        
        self.populate_tests_tree()
    
    def populate_tests_tree(self, data=None):
        """Populate lab tests treeview"""
        # Clear existing items
        for item in self.tests_tree.get_children():
            self.tests_tree.delete(item)
        
        data = data or self.tests_data
        
        for test in data:
            (id, test_id, test_name, test_type, status, ordered_date, completed_date, 
             results, normal_range, notes, p_fname, p_lname, patient_id, d_fname, d_lname) = test
            
            # Format dates
            ordered_date_str = datetime.strptime(ordered_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            completed_date_str = ""
            if completed_date:
                completed_date_str = datetime.strptime(completed_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            
            patient_name = f"{p_fname} {p_lname} ({patient_id})"
            doctor_name = f"Dr. {d_fname} {d_lname}"
            
            # Color code by status
            tags = []
            if status == "completed":
                tags = ["completed"]
            elif status == "in_progress":
                tags = ["in_progress"]
            
            self.tests_tree.insert("", "end", values=(
                id, test_id, patient_name, test_name, test_type.title(), 
                doctor_name, status.replace("_", " ").title(), ordered_date_str, completed_date_str
            ), tags=tags)
        
        # Configure tags
        self.tests_tree.tag_configure("completed", background="#d4edda")
        self.tests_tree.tag_configure("in_progress", background="#fff3cd")
    
    def on_status_filter(self, event=None):
        """Handle status filter"""
        selected_status = self.status_filter.get().lower().replace(" ", "_")
        
        if selected_status == "all":
            self.populate_tests_tree()
            return
        
        filtered_data = []
        for test in self.tests_data:
            if test[4].lower() == selected_status:
                filtered_data.append(test)
        
        self.populate_tests_tree(filtered_data)
    
    def on_type_filter(self, event=None):
        """Handle type filter"""
        selected_type = self.type_filter.get().lower()
        
        if selected_type == "all":
            self.populate_tests_tree()
            return
        
        filtered_data = []
        for test in self.tests_data:
            if test[3].lower() == selected_type:
                filtered_data.append(test)
        
        self.populate_tests_tree(filtered_data)
    
    def on_date_filter(self, event=None):
        """Handle date filter"""
        selected_date = self.date_filter.get_date()
        
        filtered_data = []
        for test in self.tests_data:
            test_date = datetime.strptime(test[5], "%Y-%m-%d %H:%M:%S").date()
            if test_date == selected_date:
                filtered_data.append(test)
        
        self.populate_tests_tree(filtered_data)
    
    def on_search(self, *args):
        """Handle search"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.populate_tests_tree()
            return
        
        filtered_data = []
        for test in self.tests_data:
            test_id = test[1].lower()
            patient_name = f"{test[10]} {test[11]}".lower()
            patient_id = test[12].lower()
            test_name = test[2].lower()
            
            if (search_term in test_id or 
                search_term in patient_name or 
                search_term in patient_id or
                search_term in test_name):
                filtered_data.append(test)
        
        self.populate_tests_tree(filtered_data)
    
    def on_test_select(self, event):
        """Handle test selection"""
        selection = self.tests_tree.selection()
        if selection:
            item = self.tests_tree.item(selection[0])
            test_id = item['values'][0]
            
            # Find selected test data
            for test in self.tests_data:
                if test[0] == test_id:
                    self.selected_test = test
                    break
    
    def sort_tests(self, column):
        """Sort tests by column"""
        # Implementation for sorting
        pass
    
    def order_test(self):
        """Order new lab test"""
        LabTestFormWindow(self, "Order Lab Test")
    
    def edit_test(self):
        """Edit selected test"""
        if not self.selected_test:
            messagebox.showwarning("Warning", "Please select a test to edit")
            return
        
        if self.selected_test[4] == "completed":
            messagebox.showwarning("Warning", "Cannot edit completed tests")
            return
        
        LabTestFormWindow(self, "Edit Lab Test", self.selected_test)
    
    def add_results(self):
        """Add results to selected test"""
        if not self.selected_test:
            messagebox.showwarning("Warning", "Please select a test to add results")
            return
        
        if self.selected_test[4] == "completed":
            messagebox.showwarning("Warning", "Test is already completed")
            return
        
        TestResultsWindow(self, self.selected_test)
    
    def complete_test(self):
        """Mark test as completed"""
        if not self.selected_test:
            messagebox.showwarning("Warning", "Please select a test to complete")
            return
        
        if self.selected_test[4] == "completed":
            messagebox.showwarning("Warning", "Test is already completed")
            return
        
        if not self.selected_test[7]:  # No results
            result = messagebox.askyesno(
                "No Results", 
                "This test has no results. Do you want to complete it anyway?"
            )
            if not result:
                return
        
        patient_name = f"{self.selected_test[10]} {self.selected_test[11]}"
        result = messagebox.askyesno(
            "Confirm Completion", 
            f"Mark test '{self.selected_test[2]}' for {patient_name} as completed?"
        )
        
        if result:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE lab_test SET 
                        status = 'completed', 
                        completed_date = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (self.selected_test[0],))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Test marked as completed")
                self.load_tests()
                self.selected_test = None
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to complete test: {str(e)}")
    
    def view_test(self):
        """View test details"""
        if not self.selected_test:
            messagebox.showwarning("Warning", "Please select a test to view")
            return
        
        LabTestDetailsWindow(self.selected_test, self.db)

class LabTestFormWindow:
    """Lab test form window for order/edit"""
    
    def __init__(self, parent, title, test_data=None):
        self.parent = parent
        self.test_data = test_data
        self.is_edit = test_data is not None
        
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.geometry("600x700")
        self.window.configure(bg=ModernStyle.BG_PRIMARY)
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Make modal
        self.window.transient(parent.parent)
        self.window.grab_set()
        
        self.create_form()
        
        if self.is_edit:
            self.populate_form()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"600x700+{x}+{y}")
    
    def create_form(self):
        """Create lab test form"""
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form card
        form_card = ModernWidget.create_card(main_frame, "Lab Test Information")
        form_card.pack(fill="both", expand=True)
        
        # Scrollable frame
        canvas = tk.Canvas(form_card, bg=ModernStyle.BG_SECONDARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_card, orient="vertical", command=canvas.yview)
        scrollable_frame = ModernWidget.create_frame(canvas, ModernStyle.BG_SECONDARY)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Form fields
        self.create_form_fields(scrollable_frame)
        
        # Buttons
        btn_frame = ModernWidget.create_frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        save_btn = ModernWidget.create_button(btn_frame, "💾 Save", self.save_test, style="success")
        save_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = ModernWidget.create_button(btn_frame, "❌ Cancel", self.window.destroy, style="secondary")
        cancel_btn.pack(side="right")
    
    def create_form_fields(self, parent):
        """Create form fields"""
        # Patient selection
        patient_frame = ModernWidget.create_frame(parent)
        patient_frame.pack(fill="x", pady=10)
        
        patient_label = ModernWidget.create_label(patient_frame, "Patient *")
        patient_label.pack(anchor="w")
        
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(
            patient_frame,
            textvariable=self.patient_var,
            state="readonly",
            width=60
        )
        self.patient_combo.pack(fill="x", pady=(5, 0))
        
        # Load patients
        self.load_patients()
        
        # Test name
        name_frame = ModernWidget.create_frame(parent)
        name_frame.pack(fill="x", pady=10)
        
        name_label = ModernWidget.create_label(name_frame, "Test Name *")
        name_label.pack(anchor="w")
        
        self.name_var = tk.StringVar()
        name_combo = ttk.Combobox(
            name_frame,
            textvariable=self.name_var,
            values=[
                "Complete Blood Count (CBC)",
                "Blood Glucose",
                "Lipid Profile",
                "Liver Function Test",
                "Kidney Function Test",
                "Thyroid Function Test",
                "Urine Analysis",
                "Chest X-Ray",
                "ECG",
                "Echocardiogram",
                "CT Scan",
                "MRI",
                "Ultrasound",
                "Mammography",
                "Colonoscopy",
                "Endoscopy"
            ],
            width=60
        )
        name_combo.pack(fill="x", pady=(5, 0))
        
        # Test type
        type_frame = ModernWidget.create_frame(parent)
        type_frame.pack(fill="x", pady=10)
        
        type_label = ModernWidget.create_label(type_frame, "Test Type *")
        type_label.pack(anchor="w")
        
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.type_var,
            values=["Blood", "Urine", "X-Ray", "MRI", "CT Scan", "ECG", "Ultrasound", "Other"],
            state="readonly",
            width=60
        )
        type_combo.pack(fill="x", pady=(5, 0))
        
        # Ordered by (Doctor)
        doctor_frame = ModernWidget.create_frame(parent)
        doctor_frame.pack(fill="x", pady=10)
        
        doctor_label = ModernWidget.create_label(doctor_frame, "Ordered By *")
        doctor_label.pack(anchor="w")
        
        self.doctor_var = tk.StringVar()
        self.doctor_combo = ttk.Combobox(
            doctor_frame,
            textvariable=self.doctor_var,
            state="readonly",
            width=60
        )
        self.doctor_combo.pack(fill="x", pady=(5, 0))
        
        # Load doctors
        self.load_doctors()
        
        # Normal range
        range_frame = ModernWidget.create_frame(parent)
        range_frame.pack(fill="x", pady=10)
        
        range_label = ModernWidget.create_label(range_frame, "Normal Range")
        range_label.pack(anchor="w")
        
        self.range_var = tk.StringVar()
        range_entry = ModernWidget.create_entry(range_frame, width=60)
        range_entry.pack(fill="x", pady=(5, 0))
        range_entry.config(textvariable=self.range_var)
        
        # Notes
        notes_frame = ModernWidget.create_frame(parent)
        notes_frame.pack(fill="both", expand=True, pady=10)
        
        notes_label = ModernWidget.create_label(notes_frame, "Notes")
        notes_label.pack(anchor="w")
        
        self.notes_text = ModernWidget.create_text(notes_frame, height=6)
        self.notes_text.pack(fill="both", expand=True, pady=(5, 0))
    
    def load_patients(self):
        """Load patients for selection"""
        conn = self.parent.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, patient_id, first_name, last_name
            FROM patient
            ORDER BY first_name, last_name
        ''')
        
        patients = cursor.fetchall()
        conn.close()
        
        self.patients_data = {}
        patient_options = []
        
        for patient in patients:
            id, patient_id, first_name, last_name = patient
            display_name = f"{first_name} {last_name} ({patient_id})"
            patient_options.append(display_name)
            self.patients_data[display_name] = id
        
        self.patient_combo['values'] = patient_options
    
    def load_doctors(self):
        """Load doctors for selection"""
        conn = self.parent.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, first_name, last_name
            FROM user
            WHERE role IN ('doctor', 'admin')
            ORDER BY first_name, last_name
        ''')
        
        doctors = cursor.fetchall()
        conn.close()
        
        self.doctors_data = {}
        doctor_options = []
        
        for doctor in doctors:
            id, first_name, last_name = doctor
            display_name = f"Dr. {first_name} {last_name}"
            doctor_options.append(display_name)
            self.doctors_data[display_name] = id
        
        self.doctor_combo['values'] = doctor_options
        
        # Set current user as default if they are a doctor
        if self.parent.current_user['role'] in ['doctor', 'admin']:
            current_doctor = f"Dr. {self.parent.current_user['first_name']} {self.parent.current_user['last_name']}"
            if current_doctor in doctor_options:
                self.doctor_var.set(current_doctor)
    
    def populate_form(self):
        """Populate form with test data"""
        if not self.test_data:
            return
        
        # Get full test data
        conn = self.parent.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT lt.*, p.first_name, p.last_name, p.patient_id,
                   u.first_name, u.last_name
            FROM lab_test lt
            JOIN patient p ON lt.patient_id = p.id
            JOIN user u ON lt.ordered_by = u.id
            WHERE lt.id = ?
        ''', (self.test_data[0],))
        
        full_data = cursor.fetchone()
        conn.close()
        
        if full_data:
            # Set patient
            patient_display = f"{full_data[11]} {full_data[12]} ({full_data[13]})"
            self.patient_var.set(patient_display)
            
            # Set test details
            self.name_var.set(full_data[2])
            self.type_var.set(full_data[3])
            
            # Set doctor
            doctor_display = f"Dr. {full_data[14]} {full_data[15]}"
            self.doctor_var.set(doctor_display)
            
            # Set other fields
            self.range_var.set(full_data[8] or "")
            
            if full_data[9]:
                self.notes_text.insert("1.0", full_data[9])
    
    def save_test(self):
        """Save lab test data"""
        # Validate required fields
        if not self.patient_var.get():
            messagebox.showerror("Error", "Please select a patient")
            return
        
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Please enter test name")
            return
        
        if not self.type_var.get():
            messagebox.showerror("Error", "Please select test type")
            return
        
        if not self.doctor_var.get():
            messagebox.showerror("Error", "Please select ordering doctor")
            return
        
        try:
            patient_id = self.patients_data[self.patient_var.get()]
            doctor_id = self.doctors_data[self.doctor_var.get()]
            
            conn = self.parent.db.get_connection()
            cursor = conn.cursor()
            
            notes = self.notes_text.get("1.0", tk.END).strip() or None
            normal_range = self.range_var.get().strip() or None
            
            if self.is_edit:
                # Update existing test
                cursor.execute('''
                    UPDATE lab_test SET
                        patient_id = ?, test_name = ?, test_type = ?, ordered_by = ?,
                        normal_range = ?, notes = ?
                    WHERE id = ?
                ''', (
                    patient_id, self.name_var.get().strip(), self.type_var.get(),
                    doctor_id, normal_range, notes, self.test_data[0]
                ))
                
                message = "Lab test updated successfully"
            else:
                # Generate test ID
                cursor.execute("SELECT COUNT(*) FROM lab_test")
                count = cursor.fetchone()[0]
                test_id = f"T{count + 1:06d}"
                
                # Insert new test
                cursor.execute('''
                    INSERT INTO lab_test (
                        test_id, patient_id, test_name, test_type, ordered_by,
                        normal_range, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    test_id, patient_id, self.name_var.get().strip(), self.type_var.get(),
                    doctor_id, normal_range, notes
                ))
                
                message = "Lab test ordered successfully"
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", message)
            self.parent.load_tests()
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save lab test: {str(e)}")

class TestResultsWindow:
    """Test results entry window"""
    
    def __init__(self, parent, test_data):
        self.parent = parent
        self.test_data = test_data
        
        self.window = tk.Toplevel()
        self.window.title("Add Test Results")
        self.window.geometry("600x500")
        self.window.configure(bg=ModernStyle.BG_PRIMARY)
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Make modal
        self.window.transient(parent.parent)
        self.window.grab_set()
        
        self.create_form()
        self.populate_existing_results()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"600x500+{x}+{y}")
    
    def create_form(self):
        """Create results form"""
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form card
        form_card = ModernWidget.create_card(main_frame, "Test Results")
        form_card.pack(fill="both", expand=True)
        
        form_frame = ModernWidget.create_frame(form_card)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Test info
        info_frame = ModernWidget.create_frame(form_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        test_label = ModernWidget.create_label(info_frame, f"Test: {self.test_data[2]}", size="large")
        test_label.pack(anchor="w")
        
        patient_label = ModernWidget.create_label(
            info_frame, 
            f"Patient: {self.test_data[10]} {self.test_data[11]} ({self.test_data[12]})",
            style="secondary"
        )
        patient_label.pack(anchor="w")
        
        # Normal range
        if self.test_data[8]:
            range_label = ModernWidget.create_label(
                info_frame, 
                f"Normal Range: {self.test_data[8]}",
                style="info"
            )
            range_label.pack(anchor="w")
        
        # Results
        results_frame = ModernWidget.create_frame(form_frame)
        results_frame.pack(fill="both", expand=True, pady=10)
        
        results_label = ModernWidget.create_label(results_frame, "Test Results *")
        results_label.pack(anchor="w")
        
        self.results_text = ModernWidget.create_text(results_frame, height=12)
        self.results_text.pack(fill="both", expand=True, pady=(5, 0))
        
        # Status
        status_frame = ModernWidget.create_frame(form_frame)
        status_frame.pack(fill="x", pady=10)
        
        status_label = ModernWidget.create_label(status_frame, "Status")
        status_label.pack(anchor="w")
        
        self.status_var = tk.StringVar(value="in_progress")
        status_combo = ttk.Combobox(
            status_frame,
            textvariable=self.status_var,
            values=["in_progress", "completed"],
            state="readonly"
        )
        status_combo.pack(anchor="w", pady=(5, 0))
        
        # Buttons
        btn_frame = ModernWidget.create_frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        save_btn = ModernWidget.create_button(btn_frame, "💾 Save Results", self.save_results, style="success")
        save_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = ModernWidget.create_button(btn_frame, "❌ Cancel", self.window.destroy, style="secondary")
        cancel_btn.pack(side="right")
    
    def populate_existing_results(self):
        """Populate existing results if any"""
        if self.test_data[7]:  # Has results
            self.results_text.insert("1.0", self.test_data[7])
        
        # Set current status
        self.status_var.set(self.test_data[4])
    
    def save_results(self):
        """Save test results"""
        results = self.results_text.get("1.0", tk.END).strip()
        
        if not results:
            messagebox.showerror("Error", "Please enter test results")
            return
        
        try:
            conn = self.parent.db.get_connection()
            cursor = conn.cursor()
            
            status = self.status_var.get()
            completed_date = None
            
            if status == "completed":
                completed_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
                UPDATE lab_test SET
                    results = ?, status = ?, completed_date = ?
                WHERE id = ?
            ''', (results, status, completed_date, self.test_data[0]))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Test results saved successfully")
            self.parent.load_tests()
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {str(e)}")

class LabTestDetailsWindow:
    """Lab test details view window"""
    
    def __init__(self, test_data, db):
        self.test_data = test_data
        self.db = db
        
        self.window = tk.Toplevel()
        self.window.title("Lab Test Details")
        self.window.geometry("700x600")
        self.window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Center window
        self.center_window()
        
        self.create_details_view()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"700x600+{x}+{y}")
    
    def create_details_view(self):
        """Create test details view"""
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ModernWidget.create_frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ModernWidget.create_label(
            title_frame, 
            f"Lab Test Details - {self.test_data[1]}", 
            size="title"
        )
        title_label.pack(side="left")
        
        close_btn = ModernWidget.create_button(title_frame, "❌ Close", self.window.destroy, style="secondary")
        close_btn.pack(side="right")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Test info tab
        info_tab = ModernWidget.create_frame(notebook)
        notebook.add(info_tab, text="Test Information")
        
        # Results tab
        results_tab = ModernWidget.create_frame(notebook)
        notebook.add(results_tab, text="Results")
        
        # Populate tabs
        self.populate_info_tab(info_tab)
        self.populate_results_tab(results_tab)
    
    def populate_info_tab(self, parent):
        """Populate test information tab"""
        info_frame = ModernWidget.create_card(parent, "Test Information")
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        details_frame = ModernWidget.create_frame(info_frame)
        details_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Parse data
        (id, test_id, test_name, test_type, status, ordered_date, completed_date, 
         results, normal_range, notes, p_fname, p_lname, patient_id, d_fname, d_lname) = self.test_data
        
        # Format dates
        ordered_date_str = datetime.strptime(ordered_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
        completed_date_str = "Not completed"
        if completed_date:
            completed_date_str = datetime.strptime(completed_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
        
        # Create info grid
        info_items = [
            ("Test ID:", test_id),
            ("Test Name:", test_name),
            ("Test Type:", test_type.title()),
            ("Status:", status.replace("_", " ").title()),
            ("Patient:", f"{p_fname} {p_lname} ({patient_id})"),
            ("Ordered By:", f"Dr. {d_fname} {d_lname}"),
            ("Ordered Date:", ordered_date_str),
            ("Completed Date:", completed_date_str),
            ("Normal Range:", normal_range or "Not specified"),
        ]
        
        for i, (label, value) in enumerate(info_items):
            row = i // 2
            col = i % 2
            
            item_frame = ModernWidget.create_frame(details_frame)
            item_frame.grid(row=row, column=col, sticky="ew", padx=10, pady=5)
            
            label_widget = ModernWidget.create_label(item_frame, label, style="secondary")
            label_widget.pack(anchor="w")
            
            value_widget = ModernWidget.create_label(item_frame, str(value))
            value_widget.pack(anchor="w")
        
        # Configure grid weights
        details_frame.grid_columnconfigure(0, weight=1)
        details_frame.grid_columnconfigure(1, weight=1)
        
        # Notes section
        if notes:
            notes_frame = ModernWidget.create_frame(details_frame)
            notes_frame.grid(row=len(info_items)//2 + 1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
            
            notes_label = ModernWidget.create_label(notes_frame, "Notes:", style="secondary")
            notes_label.pack(anchor="w")
            
            notes_text = tk.Text(
                notes_frame,
                height=4,
                bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.TEXT_PRIMARY,
                font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
                relief="flat",
                borderwidth=1,
                state="disabled"
            )
            notes_text.pack(fill="x", pady=(5, 0))
            
            notes_text.config(state="normal")
            notes_text.insert("1.0", notes)
            notes_text.config(state="disabled")
    
    def populate_results_tab(self, parent):
        """Populate results tab"""
        results_frame = ModernWidget.create_card(parent, "Test Results")
        results_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        content_frame = ModernWidget.create_frame(results_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if self.test_data[7]:  # Has results
            # Normal range
            if self.test_data[8]:
                range_label = ModernWidget.create_label(
                    content_frame, 
                    f"Normal Range: {self.test_data[8]}",
                    style="info",
                    size="large"
                )
                range_label.pack(anchor="w", pady=(0, 10))
            
            # Results
            results_label = ModernWidget.create_label(content_frame, "Results:", style="secondary")
            results_label.pack(anchor="w")
            
            results_text = tk.Text(
                content_frame,
                bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.TEXT_PRIMARY,
                font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
                relief="flat",
                borderwidth=1,
                state="disabled"
            )
            results_text.pack(fill="both", expand=True, pady=(5, 0))
            
            results_text.config(state="normal")
            results_text.insert("1.0", self.test_data[7])
            results_text.config(state="disabled")
        else:
            no_results_label = ModernWidget.create_label(
                content_frame, 
                "No results available yet",
                style="secondary",
                size="large"
            )
            no_results_label.pack(expand=True)