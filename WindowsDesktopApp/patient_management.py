"""
Patient Management Module
Advanced patient management with modern UI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
import sqlite3
from desktop_app import ModernWidget, ModernStyle

class PatientManagement:
    """Patient management interface"""
    
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        self.patients_data = []
        self.selected_patient = None
        
        self.create_interface()
        self.load_patients()
    
    def create_interface(self):
        """Create patient management interface"""
        # Title
        title_frame = ModernWidget.create_frame(self.parent)
        title_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ModernWidget.create_label(title_frame, "Patient Management", size="title")
        title_label.pack(side="left")
        
        # Action buttons
        btn_frame = ModernWidget.create_frame(title_frame)
        btn_frame.pack(side="right")
        
        add_btn = ModernWidget.create_button(btn_frame, "➕ Add Patient", self.add_patient, style="success")
        add_btn.pack(side="left", padx=(0, 10))
        
        edit_btn = ModernWidget.create_button(btn_frame, "✏️ Edit", self.edit_patient, style="primary")
        edit_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ModernWidget.create_button(btn_frame, "🗑️ Delete", self.delete_patient, style="danger")
        delete_btn.pack(side="left", padx=(0, 10))
        
        view_btn = ModernWidget.create_button(btn_frame, "👁️ View Details", self.view_patient, style="info")
        view_btn.pack(side="left")
        
        # Search frame
        search_frame = ModernWidget.create_frame(self.parent)
        search_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        search_label = ModernWidget.create_label(search_frame, "Search:")
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        search_entry = ModernWidget.create_entry(search_frame, "Enter patient name, ID, or phone...", width=40)
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.config(textvariable=self.search_var)
        
        refresh_btn = ModernWidget.create_button(search_frame, "🔄 Refresh", self.load_patients, style="secondary")
        refresh_btn.pack(side="left")
        
        # Patients list
        list_frame = ModernWidget.create_card(self.parent, "Patients List")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create treeview
        self.create_patients_tree(list_frame)
    
    def create_patients_tree(self, parent):
        """Create patients treeview"""
        tree_frame = ModernWidget.create_frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Columns
        columns = ("ID", "Patient ID", "Name", "Age", "Gender", "Phone", "Email", "Blood Type", "Last Visit")
        self.patients_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        column_widths = {"ID": 50, "Patient ID": 100, "Name": 150, "Age": 60, "Gender": 80, 
                        "Phone": 120, "Email": 150, "Blood Type": 80, "Last Visit": 100}
        
        for col in columns:
            self.patients_tree.heading(col, text=col, command=lambda c=col: self.sort_patients(c))
            self.patients_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.patients_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.patients_tree.xview)
        
        self.patients_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.patients_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Bind selection event
        self.patients_tree.bind("<<TreeviewSelect>>", self.on_patient_select)
        self.patients_tree.bind("<Double-1>", lambda e: self.view_patient())
    
    def load_patients(self):
        """Load patients from database"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.patient_id, p.first_name, p.last_name, p.date_of_birth, 
                   p.gender, p.phone, p.email, p.blood_type, p.created_at,
                   MAX(a.appointment_date) as last_visit
            FROM patient p
            LEFT JOIN appointment a ON p.id = a.patient_id
            GROUP BY p.id
            ORDER BY p.created_at DESC
        ''')
        
        self.patients_data = cursor.fetchall()
        conn.close()
        
        self.populate_patients_tree()
    
    def populate_patients_tree(self, data=None):
        """Populate patients treeview"""
        # Clear existing items
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        data = data or self.patients_data
        
        for patient in data:
            (id, patient_id, first_name, last_name, dob, gender, phone, email, 
             blood_type, created_at, last_visit) = patient
            
            # Calculate age
            age = self.calculate_age(dob)
            name = f"{first_name} {last_name}"
            
            # Format last visit
            if last_visit:
                last_visit_date = datetime.strptime(last_visit, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            else:
                last_visit_date = "Never"
            
            self.patients_tree.insert("", "end", values=(
                id, patient_id, name, age, gender.title(), 
                phone or "N/A", email or "N/A", blood_type or "N/A", last_visit_date
            ))
    
    def calculate_age(self, birth_date):
        """Calculate age from birth date"""
        if isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        
        today = datetime.now().date()
        age = today.year - birth_date.year
        
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        
        return age
    
    def on_search(self, *args):
        """Handle search"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.populate_patients_tree()
            return
        
        filtered_data = []
        for patient in self.patients_data:
            (id, patient_id, first_name, last_name, dob, gender, phone, email, 
             blood_type, created_at, last_visit) = patient
            
            name = f"{first_name} {last_name}".lower()
            
            if (search_term in name or 
                search_term in patient_id.lower() or 
                (phone and search_term in phone.lower()) or
                (email and search_term in email.lower())):
                filtered_data.append(patient)
        
        self.populate_patients_tree(filtered_data)
    
    def on_patient_select(self, event):
        """Handle patient selection"""
        selection = self.patients_tree.selection()
        if selection:
            item = self.patients_tree.item(selection[0])
            patient_id = item['values'][0]
            
            # Find selected patient data
            for patient in self.patients_data:
                if patient[0] == patient_id:
                    self.selected_patient = patient
                    break
    
    def sort_patients(self, column):
        """Sort patients by column"""
        # Implementation for sorting
        pass
    
    def add_patient(self):
        """Add new patient"""
        PatientFormWindow(self, "Add Patient")
    
    def edit_patient(self):
        """Edit selected patient"""
        if not self.selected_patient:
            messagebox.showwarning("Warning", "Please select a patient to edit")
            return
        
        PatientFormWindow(self, "Edit Patient", self.selected_patient)
    
    def delete_patient(self):
        """Delete selected patient"""
        if not self.selected_patient:
            messagebox.showwarning("Warning", "Please select a patient to delete")
            return
        
        patient_name = f"{self.selected_patient[2]} {self.selected_patient[3]}"
        result = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete patient '{patient_name}'?\n\nThis will also delete all associated appointments, bills, and lab tests."
        )
        
        if result:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                patient_id = self.selected_patient[0]
                
                # Delete related records first
                cursor.execute("DELETE FROM bill_item WHERE bill_id IN (SELECT id FROM bill WHERE patient_id = ?)", (patient_id,))
                cursor.execute("DELETE FROM bill WHERE patient_id = ?", (patient_id,))
                cursor.execute("DELETE FROM appointment WHERE patient_id = ?", (patient_id,))
                cursor.execute("DELETE FROM lab_test WHERE patient_id = ?", (patient_id,))
                cursor.execute("DELETE FROM patient WHERE id = ?", (patient_id,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Patient deleted successfully")
                self.load_patients()
                self.selected_patient = None
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")
    
    def view_patient(self):
        """View patient details"""
        if not self.selected_patient:
            messagebox.showwarning("Warning", "Please select a patient to view")
            return
        
        PatientDetailsWindow(self.selected_patient, self.db)

class PatientFormWindow:
    """Patient form window for add/edit"""
    
    def __init__(self, parent, title, patient_data=None):
        self.parent = parent
        self.patient_data = patient_data
        self.is_edit = patient_data is not None
        
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
        """Create patient form"""
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form card
        form_card = ModernWidget.create_card(main_frame, "Patient Information")
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
        
        save_btn = ModernWidget.create_button(btn_frame, "💾 Save", self.save_patient, style="success")
        save_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = ModernWidget.create_button(btn_frame, "❌ Cancel", self.window.destroy, style="secondary")
        cancel_btn.pack(side="right")
    
    def create_form_fields(self, parent):
        """Create form fields"""
        self.form_vars = {}
        
        # Personal Information
        personal_frame = ModernWidget.create_frame(parent)
        personal_frame.pack(fill="x", pady=(0, 20))
        
        personal_label = ModernWidget.create_label(personal_frame, "Personal Information", size="large")
        personal_label.pack(anchor="w", pady=(0, 10))
        
        # First Name
        fname_frame = ModernWidget.create_frame(personal_frame)
        fname_frame.pack(fill="x", pady=5)
        
        fname_label = ModernWidget.create_label(fname_frame, "First Name *")
        fname_label.pack(anchor="w")
        
        self.form_vars['first_name'] = tk.StringVar()
        fname_entry = ModernWidget.create_entry(fname_frame, width=50)
        fname_entry.pack(fill="x", pady=(5, 0))
        fname_entry.config(textvariable=self.form_vars['first_name'])
        
        # Last Name
        lname_frame = ModernWidget.create_frame(personal_frame)
        lname_frame.pack(fill="x", pady=5)
        
        lname_label = ModernWidget.create_label(lname_frame, "Last Name *")
        lname_label.pack(anchor="w")
        
        self.form_vars['last_name'] = tk.StringVar()
        lname_entry = ModernWidget.create_entry(lname_frame, width=50)
        lname_entry.pack(fill="x", pady=(5, 0))
        lname_entry.config(textvariable=self.form_vars['last_name'])
        
        # Date of Birth
        dob_frame = ModernWidget.create_frame(personal_frame)
        dob_frame.pack(fill="x", pady=5)
        
        dob_label = ModernWidget.create_label(dob_frame, "Date of Birth *")
        dob_label.pack(anchor="w")
        
        self.dob_entry = DateEntry(
            dob_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.dob_entry.pack(anchor="w", pady=(5, 0))
        
        # Gender
        gender_frame = ModernWidget.create_frame(personal_frame)
        gender_frame.pack(fill="x", pady=5)
        
        gender_label = ModernWidget.create_label(gender_frame, "Gender *")
        gender_label.pack(anchor="w")
        
        self.form_vars['gender'] = tk.StringVar(value="male")
        gender_radio_frame = ModernWidget.create_frame(gender_frame)
        gender_radio_frame.pack(anchor="w", pady=(5, 0))
        
        male_radio = tk.Radiobutton(
            gender_radio_frame, text="Male", variable=self.form_vars['gender'], value="male",
            bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.TEXT_PRIMARY, selectcolor=ModernStyle.BG_DARK
        )
        male_radio.pack(side="left", padx=(0, 20))
        
        female_radio = tk.Radiobutton(
            gender_radio_frame, text="Female", variable=self.form_vars['gender'], value="female",
            bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.TEXT_PRIMARY, selectcolor=ModernStyle.BG_DARK
        )
        female_radio.pack(side="left")
        
        # Contact Information
        contact_frame = ModernWidget.create_frame(parent)
        contact_frame.pack(fill="x", pady=(20, 20))
        
        contact_label = ModernWidget.create_label(contact_frame, "Contact Information", size="large")
        contact_label.pack(anchor="w", pady=(0, 10))
        
        # Phone
        phone_frame = ModernWidget.create_frame(contact_frame)
        phone_frame.pack(fill="x", pady=5)
        
        phone_label = ModernWidget.create_label(phone_frame, "Phone")
        phone_label.pack(anchor="w")
        
        self.form_vars['phone'] = tk.StringVar()
        phone_entry = ModernWidget.create_entry(phone_frame, width=50)
        phone_entry.pack(fill="x", pady=(5, 0))
        phone_entry.config(textvariable=self.form_vars['phone'])
        
        # Email
        email_frame = ModernWidget.create_frame(contact_frame)
        email_frame.pack(fill="x", pady=5)
        
        email_label = ModernWidget.create_label(email_frame, "Email")
        email_label.pack(anchor="w")
        
        self.form_vars['email'] = tk.StringVar()
        email_entry = ModernWidget.create_entry(email_frame, width=50)
        email_entry.pack(fill="x", pady=(5, 0))
        email_entry.config(textvariable=self.form_vars['email'])
        
        # Address
        address_frame = ModernWidget.create_frame(contact_frame)
        address_frame.pack(fill="x", pady=5)
        
        address_label = ModernWidget.create_label(address_frame, "Address")
        address_label.pack(anchor="w")
        
        self.address_text = ModernWidget.create_text(address_frame, height=3)
        self.address_text.pack(fill="x", pady=(5, 0))
        
        # Emergency Contact
        emergency_frame = ModernWidget.create_frame(parent)
        emergency_frame.pack(fill="x", pady=(20, 20))
        
        emergency_label = ModernWidget.create_label(emergency_frame, "Emergency Contact", size="large")
        emergency_label.pack(anchor="w", pady=(0, 10))
        
        # Emergency Contact Name
        ec_name_frame = ModernWidget.create_frame(emergency_frame)
        ec_name_frame.pack(fill="x", pady=5)
        
        ec_name_label = ModernWidget.create_label(ec_name_frame, "Emergency Contact Name")
        ec_name_label.pack(anchor="w")
        
        self.form_vars['emergency_contact'] = tk.StringVar()
        ec_name_entry = ModernWidget.create_entry(ec_name_frame, width=50)
        ec_name_entry.pack(fill="x", pady=(5, 0))
        ec_name_entry.config(textvariable=self.form_vars['emergency_contact'])
        
        # Emergency Phone
        ec_phone_frame = ModernWidget.create_frame(emergency_frame)
        ec_phone_frame.pack(fill="x", pady=5)
        
        ec_phone_label = ModernWidget.create_label(ec_phone_frame, "Emergency Phone")
        ec_phone_label.pack(anchor="w")
        
        self.form_vars['emergency_phone'] = tk.StringVar()
        ec_phone_entry = ModernWidget.create_entry(ec_phone_frame, width=50)
        ec_phone_entry.pack(fill="x", pady=(5, 0))
        ec_phone_entry.config(textvariable=self.form_vars['emergency_phone'])
        
        # Medical Information
        medical_frame = ModernWidget.create_frame(parent)
        medical_frame.pack(fill="x", pady=(20, 20))
        
        medical_label = ModernWidget.create_label(medical_frame, "Medical Information", size="large")
        medical_label.pack(anchor="w", pady=(0, 10))
        
        # Blood Type
        blood_frame = ModernWidget.create_frame(medical_frame)
        blood_frame.pack(fill="x", pady=5)
        
        blood_label = ModernWidget.create_label(blood_frame, "Blood Type")
        blood_label.pack(anchor="w")
        
        self.form_vars['blood_type'] = tk.StringVar()
        blood_combo = ttk.Combobox(
            blood_frame,
            textvariable=self.form_vars['blood_type'],
            values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
            state="readonly"
        )
        blood_combo.pack(anchor="w", pady=(5, 0))
        
        # Allergies
        allergies_frame = ModernWidget.create_frame(medical_frame)
        allergies_frame.pack(fill="x", pady=5)
        
        allergies_label = ModernWidget.create_label(allergies_frame, "Allergies")
        allergies_label.pack(anchor="w")
        
        self.allergies_text = ModernWidget.create_text(allergies_frame, height=3)
        self.allergies_text.pack(fill="x", pady=(5, 0))
        
        # Medical History
        history_frame = ModernWidget.create_frame(medical_frame)
        history_frame.pack(fill="x", pady=5)
        
        history_label = ModernWidget.create_label(history_frame, "Medical History")
        history_label.pack(anchor="w")
        
        self.history_text = ModernWidget.create_text(history_frame, height=4)
        self.history_text.pack(fill="x", pady=(5, 0))
    
    def populate_form(self):
        """Populate form with patient data"""
        if not self.patient_data:
            return
        
        (id, patient_id, first_name, last_name, dob, gender, phone, email, 
         blood_type, created_at, last_visit, address, emergency_contact, 
         emergency_phone, allergies, medical_history) = self.patient_data + (None,) * 6
        
        # Get full patient data
        conn = self.parent.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT address, emergency_contact, emergency_phone, allergies, medical_history
            FROM patient WHERE id = ?
        ''', (id,))
        
        additional_data = cursor.fetchone()
        conn.close()
        
        if additional_data:
            address, emergency_contact, emergency_phone, allergies, medical_history = additional_data
        
        # Populate fields
        self.form_vars['first_name'].set(first_name or "")
        self.form_vars['last_name'].set(last_name or "")
        
        if dob:
            self.dob_entry.set_date(datetime.strptime(dob, "%Y-%m-%d").date())
        
        self.form_vars['gender'].set(gender or "male")
        self.form_vars['phone'].set(phone or "")
        self.form_vars['email'].set(email or "")
        
        if address:
            self.address_text.insert("1.0", address)
        
        self.form_vars['emergency_contact'].set(emergency_contact or "")
        self.form_vars['emergency_phone'].set(emergency_phone or "")
        self.form_vars['blood_type'].set(blood_type or "")
        
        if allergies:
            self.allergies_text.insert("1.0", allergies)
        
        if medical_history:
            self.history_text.insert("1.0", medical_history)
    
    def save_patient(self):
        """Save patient data"""
        # Validate required fields
        if not self.form_vars['first_name'].get().strip():
            messagebox.showerror("Error", "First name is required")
            return
        
        if not self.form_vars['last_name'].get().strip():
            messagebox.showerror("Error", "Last name is required")
            return
        
        try:
            conn = self.parent.db.get_connection()
            cursor = conn.cursor()
            
            # Prepare data
            data = {
                'first_name': self.form_vars['first_name'].get().strip(),
                'last_name': self.form_vars['last_name'].get().strip(),
                'date_of_birth': self.dob_entry.get_date().strftime('%Y-%m-%d'),
                'gender': self.form_vars['gender'].get(),
                'phone': self.form_vars['phone'].get().strip() or None,
                'email': self.form_vars['email'].get().strip() or None,
                'address': self.address_text.get("1.0", tk.END).strip() or None,
                'emergency_contact': self.form_vars['emergency_contact'].get().strip() or None,
                'emergency_phone': self.form_vars['emergency_phone'].get().strip() or None,
                'blood_type': self.form_vars['blood_type'].get() or None,
                'allergies': self.allergies_text.get("1.0", tk.END).strip() or None,
                'medical_history': self.history_text.get("1.0", tk.END).strip() or None
            }
            
            if self.is_edit:
                # Update existing patient
                cursor.execute('''
                    UPDATE patient SET
                        first_name = ?, last_name = ?, date_of_birth = ?, gender = ?,
                        phone = ?, email = ?, address = ?, emergency_contact = ?,
                        emergency_phone = ?, blood_type = ?, allergies = ?, medical_history = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (
                    data['first_name'], data['last_name'], data['date_of_birth'], data['gender'],
                    data['phone'], data['email'], data['address'], data['emergency_contact'],
                    data['emergency_phone'], data['blood_type'], data['allergies'], data['medical_history'],
                    self.patient_data[0]
                ))
                
                message = "Patient updated successfully"
            else:
                # Generate patient ID
                cursor.execute("SELECT COUNT(*) FROM patient")
                count = cursor.fetchone()[0]
                patient_id = f"P{count + 1:06d}"
                
                # Insert new patient
                cursor.execute('''
                    INSERT INTO patient (
                        patient_id, first_name, last_name, date_of_birth, gender,
                        phone, email, address, emergency_contact, emergency_phone,
                        blood_type, allergies, medical_history
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    patient_id, data['first_name'], data['last_name'], data['date_of_birth'], data['gender'],
                    data['phone'], data['email'], data['address'], data['emergency_contact'],
                    data['emergency_phone'], data['blood_type'], data['allergies'], data['medical_history']
                ))
                
                message = "Patient added successfully"
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", message)
            self.parent.load_patients()
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save patient: {str(e)}")

class PatientDetailsWindow:
    """Patient details view window"""
    
    def __init__(self, patient_data, db):
        self.patient_data = patient_data
        self.db = db
        
        self.window = tk.Toplevel()
        self.window.title("Patient Details")
        self.window.geometry("800x600")
        self.window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Center window
        self.center_window()
        
        self.create_details_view()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"800x600+{x}+{y}")
    
    def create_details_view(self):
        """Create patient details view"""
        # Get full patient data
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patient WHERE id = ?
        ''', (self.patient_data[0],))
        
        full_data = cursor.fetchone()
        
        # Get appointments, bills, and lab tests
        cursor.execute('''
            SELECT COUNT(*) FROM appointment WHERE patient_id = ?
        ''', (self.patient_data[0],))
        appointments_count = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM bill WHERE patient_id = ?
        ''', (self.patient_data[0],))
        bills_count = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM lab_test WHERE patient_id = ?
        ''', (self.patient_data[0],))
        tests_count = cursor.fetchone()[0]
        
        conn.close()
        
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ModernWidget.create_frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ModernWidget.create_label(
            title_frame, 
            f"Patient Details - {full_data[2]} {full_data[3]}", 
            size="title"
        )
        title_label.pack(side="left")
        
        close_btn = ModernWidget.create_button(title_frame, "❌ Close", self.window.destroy, style="secondary")
        close_btn.pack(side="right")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Personal info tab
        personal_tab = ModernWidget.create_frame(notebook)
        notebook.add(personal_tab, text="Personal Information")
        
        # Medical info tab
        medical_tab = ModernWidget.create_frame(notebook)
        notebook.add(medical_tab, text="Medical Information")
        
        # Summary tab
        summary_tab = ModernWidget.create_frame(notebook)
        notebook.add(summary_tab, text="Summary")
        
        # Populate tabs
        self.populate_personal_tab(personal_tab, full_data)
        self.populate_medical_tab(medical_tab, full_data)
        self.populate_summary_tab(summary_tab, appointments_count, bills_count, tests_count)
    
    def populate_personal_tab(self, parent, data):
        """Populate personal information tab"""
        info_frame = ModernWidget.create_card(parent, "Personal Information")
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        details_frame = ModernWidget.create_frame(info_frame)
        details_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create info grid
        info_items = [
            ("Patient ID:", data[1]),
            ("Full Name:", f"{data[2]} {data[3]}"),
            ("Date of Birth:", data[4]),
            ("Age:", str(self.calculate_age(data[4]))),
            ("Gender:", data[5].title()),
            ("Phone:", data[6] or "N/A"),
            ("Email:", data[7] or "N/A"),
            ("Address:", data[8] or "N/A"),
            ("Emergency Contact:", data[9] or "N/A"),
            ("Emergency Phone:", data[10] or "N/A"),
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
    
    def populate_medical_tab(self, parent, data):
        """Populate medical information tab"""
        medical_frame = ModernWidget.create_card(parent, "Medical Information")
        medical_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        details_frame = ModernWidget.create_frame(medical_frame)
        details_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Blood type
        blood_frame = ModernWidget.create_frame(details_frame)
        blood_frame.pack(fill="x", pady=10)
        
        blood_label = ModernWidget.create_label(blood_frame, "Blood Type:", style="secondary")
        blood_label.pack(anchor="w")
        
        blood_value = ModernWidget.create_label(blood_frame, data[11] or "Not specified")
        blood_value.pack(anchor="w")
        
        # Allergies
        allergies_frame = ModernWidget.create_frame(details_frame)
        allergies_frame.pack(fill="x", pady=10)
        
        allergies_label = ModernWidget.create_label(allergies_frame, "Allergies:", style="secondary")
        allergies_label.pack(anchor="w")
        
        allergies_text = tk.Text(
            allergies_frame,
            height=4,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_PRIMARY,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            relief="flat",
            borderwidth=1,
            state="disabled"
        )
        allergies_text.pack(fill="x", pady=(5, 0))
        
        if data[12]:
            allergies_text.config(state="normal")
            allergies_text.insert("1.0", data[12])
            allergies_text.config(state="disabled")
        
        # Medical history
        history_frame = ModernWidget.create_frame(details_frame)
        history_frame.pack(fill="both", expand=True, pady=10)
        
        history_label = ModernWidget.create_label(history_frame, "Medical History:", style="secondary")
        history_label.pack(anchor="w")
        
        history_text = tk.Text(
            history_frame,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_PRIMARY,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            relief="flat",
            borderwidth=1,
            state="disabled"
        )
        history_text.pack(fill="both", expand=True, pady=(5, 0))
        
        if data[13]:
            history_text.config(state="normal")
            history_text.insert("1.0", data[13])
            history_text.config(state="disabled")
    
    def populate_summary_tab(self, parent, appointments_count, bills_count, tests_count):
        """Populate summary tab"""
        summary_frame = ModernWidget.create_card(parent, "Patient Summary")
        summary_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        stats_frame = ModernWidget.create_frame(summary_frame)
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        # Statistics cards
        stats = [
            ("Total Appointments", appointments_count, ModernStyle.BTN_PRIMARY),
            ("Total Bills", bills_count, ModernStyle.BG_WARNING),
            ("Lab Tests", tests_count, ModernStyle.BG_INFO)
        ]
        
        for i, (title, value, color) in enumerate(stats):
            card = tk.Frame(
                stats_frame,
                bg=color,
                relief="flat",
                borderwidth=0,
                width=200,
                height=100
            )
            card.pack(side="left", padx=10, fill="y")
            card.pack_propagate(False)
            
            value_label = tk.Label(
                card,
                text=str(value),
                bg=color,
                fg=ModernStyle.TEXT_PRIMARY,
                font=(ModernStyle.FONT_FAMILY, 20, "bold")
            )
            value_label.pack(pady=(15, 5))
            
            title_label = tk.Label(
                card,
                text=title,
                bg=color,
                fg=ModernStyle.TEXT_PRIMARY,
                font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL)
            )
            title_label.pack()
    
    def calculate_age(self, birth_date):
        """Calculate age from birth date"""
        if isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        
        today = datetime.now().date()
        age = today.year - birth_date.year
        
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        
        return age