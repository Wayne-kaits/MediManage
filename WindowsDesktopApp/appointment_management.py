"""
Appointment Management Module
Advanced appointment scheduling with modern UI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import sqlite3
from desktop_app import ModernWidget, ModernStyle

class AppointmentManagement:
    """Appointment management interface"""
    
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        self.appointments_data = []
        self.selected_appointment = None
        
        self.create_interface()
        self.load_appointments()
    
    def create_interface(self):
        """Create appointment management interface"""
        # Title
        title_frame = ModernWidget.create_frame(self.parent)
        title_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ModernWidget.create_label(title_frame, "Appointment Management", size="title")
        title_label.pack(side="left")
        
        # Action buttons
        btn_frame = ModernWidget.create_frame(title_frame)
        btn_frame.pack(side="right")
        
        add_btn = ModernWidget.create_button(btn_frame, "➕ Schedule Appointment", self.add_appointment, style="success")
        add_btn.pack(side="left", padx=(0, 10))
        
        edit_btn = ModernWidget.create_button(btn_frame, "✏️ Edit", self.edit_appointment, style="primary")
        edit_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ModernWidget.create_button(btn_frame, "❌ Cancel", self.cancel_appointment, style="danger")
        cancel_btn.pack(side="left", padx=(0, 10))
        
        complete_btn = ModernWidget.create_button(btn_frame, "✅ Complete", self.complete_appointment, style="success")
        complete_btn.pack(side="left", padx=(0, 10))
        
        view_btn = ModernWidget.create_button(btn_frame, "👁️ View Details", self.view_appointment, style="info")
        view_btn.pack(side="left")
        
        # Filter frame
        filter_frame = ModernWidget.create_frame(self.parent)
        filter_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Date filter
        date_label = ModernWidget.create_label(filter_frame, "Filter by Date:")
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
        
        # Status filter
        status_label = ModernWidget.create_label(filter_frame, "Status:")
        status_label.pack(side="left", padx=(0, 10))
        
        self.status_filter = ttk.Combobox(
            filter_frame,
            values=["All", "Scheduled", "Completed", "Cancelled"],
            state="readonly",
            width=12
        )
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=(0, 20))
        self.status_filter.bind("<<ComboboxSelected>>", self.on_status_filter)
        
        # Search
        search_label = ModernWidget.create_label(filter_frame, "Search:")
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        search_entry = ModernWidget.create_entry(filter_frame, "Enter patient name or ID...", width=30)
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.config(textvariable=self.search_var)
        
        refresh_btn = ModernWidget.create_button(filter_frame, "🔄 Refresh", self.load_appointments, style="secondary")
        refresh_btn.pack(side="left")
        
        # Appointments list
        list_frame = ModernWidget.create_card(self.parent, "Appointments List")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create treeview
        self.create_appointments_tree(list_frame)
    
    def create_appointments_tree(self, parent):
        """Create appointments treeview"""
        tree_frame = ModernWidget.create_frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Columns
        columns = ("ID", "Date", "Time", "Patient", "Doctor", "Type", "Status", "Notes")
        self.appointments_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        column_widths = {"ID": 50, "Date": 100, "Time": 80, "Patient": 150, "Doctor": 150, 
                        "Type": 120, "Status": 100, "Notes": 200}
        
        for col in columns:
            self.appointments_tree.heading(col, text=col, command=lambda c=col: self.sort_appointments(c))
            self.appointments_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.appointments_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.appointments_tree.xview)
        
        self.appointments_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.appointments_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Bind selection event
        self.appointments_tree.bind("<<TreeviewSelect>>", self.on_appointment_select)
        self.appointments_tree.bind("<Double-1>", lambda e: self.view_appointment())
    
    def load_appointments(self):
        """Load appointments from database"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, a.appointment_date, a.appointment_type, a.status, a.notes,
                   p.first_name, p.last_name, p.patient_id,
                   u.first_name, u.last_name
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN user u ON a.doctor_id = u.id
            ORDER BY a.appointment_date DESC
        ''')
        
        self.appointments_data = cursor.fetchall()
        conn.close()
        
        self.populate_appointments_tree()
    
    def populate_appointments_tree(self, data=None):
        """Populate appointments treeview"""
        # Clear existing items
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        data = data or self.appointments_data
        
        for appointment in data:
            (id, appointment_date, appointment_type, status, notes,
             p_fname, p_lname, patient_id, d_fname, d_lname) = appointment
            
            # Format date and time
            apt_datetime = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M:%S")
            date_str = apt_datetime.strftime("%Y-%m-%d")
            time_str = apt_datetime.strftime("%H:%M")
            
            patient_name = f"{p_fname} {p_lname} ({patient_id})"
            doctor_name = f"Dr. {d_fname} {d_lname}"
            
            # Color code by status
            tags = []
            if status == "completed":
                tags = ["completed"]
            elif status == "cancelled":
                tags = ["cancelled"]
            elif apt_datetime < datetime.now():
                tags = ["overdue"]
            
            item = self.appointments_tree.insert("", "end", values=(
                id, date_str, time_str, patient_name, doctor_name, 
                appointment_type.title(), status.title(), notes or ""
            ), tags=tags)
        
        # Configure tags
        self.appointments_tree.tag_configure("completed", background="#d4edda")
        self.appointments_tree.tag_configure("cancelled", background="#f8d7da")
        self.appointments_tree.tag_configure("overdue", background="#fff3cd")
    
    def on_date_filter(self, event=None):
        """Handle date filter"""
        selected_date = self.date_filter.get_date()
        
        filtered_data = []
        for appointment in self.appointments_data:
            apt_date = datetime.strptime(appointment[1], "%Y-%m-%d %H:%M:%S").date()
            if apt_date == selected_date:
                filtered_data.append(appointment)
        
        self.populate_appointments_tree(filtered_data)
    
    def on_status_filter(self, event=None):
        """Handle status filter"""
        selected_status = self.status_filter.get().lower()
        
        if selected_status == "all":
            self.populate_appointments_tree()
            return
        
        filtered_data = []
        for appointment in self.appointments_data:
            if appointment[3].lower() == selected_status:
                filtered_data.append(appointment)
        
        self.populate_appointments_tree(filtered_data)
    
    def on_search(self, *args):
        """Handle search"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.populate_appointments_tree()
            return
        
        filtered_data = []
        for appointment in self.appointments_data:
            patient_name = f"{appointment[5]} {appointment[6]}".lower()
            patient_id = appointment[7].lower()
            
            if search_term in patient_name or search_term in patient_id:
                filtered_data.append(appointment)
        
        self.populate_appointments_tree(filtered_data)
    
    def on_appointment_select(self, event):
        """Handle appointment selection"""
        selection = self.appointments_tree.selection()
        if selection:
            item = self.appointments_tree.item(selection[0])
            appointment_id = item['values'][0]
            
            # Find selected appointment data
            for appointment in self.appointments_data:
                if appointment[0] == appointment_id:
                    self.selected_appointment = appointment
                    break
    
    def sort_appointments(self, column):
        """Sort appointments by column"""
        # Implementation for sorting
        pass
    
    def add_appointment(self):
        """Add new appointment"""
        AppointmentFormWindow(self, "Schedule Appointment")
    
    def edit_appointment(self):
        """Edit selected appointment"""
        if not self.selected_appointment:
            messagebox.showwarning("Warning", "Please select an appointment to edit")
            return
        
        if self.selected_appointment[3] in ["completed", "cancelled"]:
            messagebox.showwarning("Warning", "Cannot edit completed or cancelled appointments")
            return
        
        AppointmentFormWindow(self, "Edit Appointment", self.selected_appointment)
    
    def cancel_appointment(self):
        """Cancel selected appointment"""
        if not self.selected_appointment:
            messagebox.showwarning("Warning", "Please select an appointment to cancel")
            return
        
        if self.selected_appointment[3] in ["completed", "cancelled"]:
            messagebox.showwarning("Warning", "Appointment is already completed or cancelled")
            return
        
        patient_name = f"{self.selected_appointment[5]} {self.selected_appointment[6]}"
        result = messagebox.askyesno(
            "Confirm Cancellation", 
            f"Are you sure you want to cancel the appointment for {patient_name}?"
        )
        
        if result:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE appointment SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (self.selected_appointment[0],))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Appointment cancelled successfully")
                self.load_appointments()
                self.selected_appointment = None
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to cancel appointment: {str(e)}")
    
    def complete_appointment(self):
        """Mark appointment as completed"""
        if not self.selected_appointment:
            messagebox.showwarning("Warning", "Please select an appointment to complete")
            return
        
        if self.selected_appointment[3] == "completed":
            messagebox.showwarning("Warning", "Appointment is already completed")
            return
        
        if self.selected_appointment[3] == "cancelled":
            messagebox.showwarning("Warning", "Cannot complete a cancelled appointment")
            return
        
        patient_name = f"{self.selected_appointment[5]} {self.selected_appointment[6]}"
        result = messagebox.askyesno(
            "Confirm Completion", 
            f"Mark appointment for {patient_name} as completed?"
        )
        
        if result:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE appointment SET status = 'completed', updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (self.selected_appointment[0],))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Appointment marked as completed")
                self.load_appointments()
                self.selected_appointment = None
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to complete appointment: {str(e)}")
    
    def view_appointment(self):
        """View appointment details"""
        if not self.selected_appointment:
            messagebox.showwarning("Warning", "Please select an appointment to view")
            return
        
        AppointmentDetailsWindow(self.selected_appointment, self.db)

class AppointmentFormWindow:
    """Appointment form window for add/edit"""
    
    def __init__(self, parent, title, appointment_data=None):
        self.parent = parent
        self.appointment_data = appointment_data
        self.is_edit = appointment_data is not None
        
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.geometry("500x600")
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
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"500x600+{x}+{y}")
    
    def create_form(self):
        """Create appointment form"""
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form card
        form_card = ModernWidget.create_card(main_frame, "Appointment Information")
        form_card.pack(fill="both", expand=True)
        
        # Form container
        form_frame = ModernWidget.create_frame(form_card)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Patient selection
        patient_frame = ModernWidget.create_frame(form_frame)
        patient_frame.pack(fill="x", pady=10)
        
        patient_label = ModernWidget.create_label(patient_frame, "Patient *")
        patient_label.pack(anchor="w")
        
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(
            patient_frame,
            textvariable=self.patient_var,
            state="readonly",
            width=50
        )
        self.patient_combo.pack(fill="x", pady=(5, 0))
        
        # Load patients
        self.load_patients()
        
        # Doctor selection
        doctor_frame = ModernWidget.create_frame(form_frame)
        doctor_frame.pack(fill="x", pady=10)
        
        doctor_label = ModernWidget.create_label(doctor_frame, "Doctor *")
        doctor_label.pack(anchor="w")
        
        self.doctor_var = tk.StringVar()
        self.doctor_combo = ttk.Combobox(
            doctor_frame,
            textvariable=self.doctor_var,
            state="readonly",
            width=50
        )
        self.doctor_combo.pack(fill="x", pady=(5, 0))
        
        # Load doctors
        self.load_doctors()
        
        # Date selection
        date_frame = ModernWidget.create_frame(form_frame)
        date_frame.pack(fill="x", pady=10)
        
        date_label = ModernWidget.create_label(date_frame, "Date *")
        date_label.pack(anchor="w")
        
        self.date_entry = DateEntry(
            date_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd',
            mindate=datetime.now().date()
        )
        self.date_entry.pack(anchor="w", pady=(5, 0))
        
        # Time selection
        time_frame = ModernWidget.create_frame(form_frame)
        time_frame.pack(fill="x", pady=10)
        
        time_label = ModernWidget.create_label(time_frame, "Time *")
        time_label.pack(anchor="w")
        
        time_container = ModernWidget.create_frame(time_frame)
        time_container.pack(anchor="w", pady=(5, 0))
        
        self.hour_var = tk.StringVar(value="09")
        hour_combo = ttk.Combobox(
            time_container,
            textvariable=self.hour_var,
            values=[f"{i:02d}" for i in range(8, 18)],
            state="readonly",
            width=5
        )
        hour_combo.pack(side="left")
        
        colon_label = ModernWidget.create_label(time_container, ":")
        colon_label.pack(side="left", padx=5)
        
        self.minute_var = tk.StringVar(value="00")
        minute_combo = ttk.Combobox(
            time_container,
            textvariable=self.minute_var,
            values=["00", "15", "30", "45"],
            state="readonly",
            width=5
        )
        minute_combo.pack(side="left")
        
        # Appointment type
        type_frame = ModernWidget.create_frame(form_frame)
        type_frame.pack(fill="x", pady=10)
        
        type_label = ModernWidget.create_label(type_frame, "Appointment Type *")
        type_label.pack(anchor="w")
        
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.type_var,
            values=["Consultation", "Follow-up", "Check-up", "Emergency", "Surgery", "Therapy"],
            state="readonly",
            width=50
        )
        type_combo.pack(fill="x", pady=(5, 0))
        
        # Notes
        notes_frame = ModernWidget.create_frame(form_frame)
        notes_frame.pack(fill="both", expand=True, pady=10)
        
        notes_label = ModernWidget.create_label(notes_frame, "Notes")
        notes_label.pack(anchor="w")
        
        self.notes_text = ModernWidget.create_text(notes_frame, height=6)
        self.notes_text.pack(fill="both", expand=True, pady=(5, 0))
        
        # Buttons
        btn_frame = ModernWidget.create_frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        save_btn = ModernWidget.create_button(btn_frame, "💾 Save", self.save_appointment, style="success")
        save_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = ModernWidget.create_button(btn_frame, "❌ Cancel", self.window.destroy, style="secondary")
        cancel_btn.pack(side="right")
    
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
    
    def populate_form(self):
        """Populate form with appointment data"""
        if not self.appointment_data:
            return
        
        # Get full appointment data
        conn = self.parent.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.patient_id, a.doctor_id, a.appointment_date, a.appointment_type, a.notes,
                   p.first_name, p.last_name, p.patient_id,
                   u.first_name, u.last_name
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN user u ON a.doctor_id = u.id
            WHERE a.id = ?
        ''', (self.appointment_data[0],))
        
        full_data = cursor.fetchone()
        conn.close()
        
        if full_data:
            (patient_id, doctor_id, appointment_date, appointment_type, notes,
             p_fname, p_lname, p_id, d_fname, d_lname) = full_data
            
            # Set patient
            patient_display = f"{p_fname} {p_lname} ({p_id})"
            self.patient_var.set(patient_display)
            
            # Set doctor
            doctor_display = f"Dr. {d_fname} {d_lname}"
            self.doctor_var.set(doctor_display)
            
            # Set date and time
            apt_datetime = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M:%S")
            self.date_entry.set_date(apt_datetime.date())
            self.hour_var.set(f"{apt_datetime.hour:02d}")
            self.minute_var.set(f"{apt_datetime.minute:02d}")
            
            # Set type
            self.type_var.set(appointment_type)
            
            # Set notes
            if notes:
                self.notes_text.insert("1.0", notes)
    
    def save_appointment(self):
        """Save appointment data"""
        # Validate required fields
        if not self.patient_var.get():
            messagebox.showerror("Error", "Please select a patient")
            return
        
        if not self.doctor_var.get():
            messagebox.showerror("Error", "Please select a doctor")
            return
        
        if not self.type_var.get():
            messagebox.showerror("Error", "Please select appointment type")
            return
        
        try:
            # Get patient and doctor IDs
            patient_id = self.patients_data[self.patient_var.get()]
            doctor_id = self.doctors_data[self.doctor_var.get()]
            
            # Create appointment datetime
            appointment_date = self.date_entry.get_date()
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            appointment_datetime = datetime.combine(appointment_date, datetime.min.time().replace(hour=hour, minute=minute))
            
            # Check if appointment time is in the past
            if appointment_datetime < datetime.now():
                messagebox.showerror("Error", "Cannot schedule appointment in the past")
                return
            
            # Check for conflicts
            if not self.is_edit or self.appointment_data[0] != patient_id:
                if self.check_appointment_conflict(doctor_id, appointment_datetime):
                    messagebox.showerror("Error", "Doctor already has an appointment at this time")
                    return
            
            conn = self.parent.db.get_connection()
            cursor = conn.cursor()
            
            notes = self.notes_text.get("1.0", tk.END).strip() or None
            
            if self.is_edit:
                # Update existing appointment
                cursor.execute('''
                    UPDATE appointment SET
                        patient_id = ?, doctor_id = ?, appointment_date = ?, 
                        appointment_type = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (
                    patient_id, doctor_id, appointment_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    self.type_var.get(), notes, self.appointment_data[0]
                ))
                
                message = "Appointment updated successfully"
            else:
                # Insert new appointment
                cursor.execute('''
                    INSERT INTO appointment (
                        patient_id, doctor_id, appointment_date, appointment_type, notes
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    patient_id, doctor_id, appointment_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    self.type_var.get(), notes
                ))
                
                message = "Appointment scheduled successfully"
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", message)
            self.parent.load_appointments()
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save appointment: {str(e)}")
    
    def check_appointment_conflict(self, doctor_id, appointment_datetime):
        """Check for appointment conflicts"""
        conn = self.parent.db.get_connection()
        cursor = conn.cursor()
        
        # Check for appointments within 30 minutes
        start_time = appointment_datetime - timedelta(minutes=30)
        end_time = appointment_datetime + timedelta(minutes=30)
        
        cursor.execute('''
            SELECT COUNT(*) FROM appointment
            WHERE doctor_id = ? AND status = 'scheduled'
            AND appointment_date BETWEEN ? AND ?
        ''', (doctor_id, start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0

class AppointmentDetailsWindow:
    """Appointment details view window"""
    
    def __init__(self, appointment_data, db):
        self.appointment_data = appointment_data
        self.db = db
        
        self.window = tk.Toplevel()
        self.window.title("Appointment Details")
        self.window.geometry("600x500")
        self.window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Center window
        self.center_window()
        
        self.create_details_view()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"600x500+{x}+{y}")
    
    def create_details_view(self):
        """Create appointment details view"""
        # Get full appointment data
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, p.first_name, p.last_name, p.patient_id, p.phone, p.email,
                   u.first_name, u.last_name
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN user u ON a.doctor_id = u.id
            WHERE a.id = ?
        ''', (self.appointment_data[0],))
        
        full_data = cursor.fetchone()
        conn.close()
        
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ModernWidget.create_frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ModernWidget.create_label(
            title_frame, 
            "Appointment Details", 
            size="title"
        )
        title_label.pack(side="left")
        
        close_btn = ModernWidget.create_button(title_frame, "❌ Close", self.window.destroy, style="secondary")
        close_btn.pack(side="right")
        
        # Details card
        details_card = ModernWidget.create_card(main_frame, "Appointment Information")
        details_card.pack(fill="both", expand=True)
        
        details_frame = ModernWidget.create_frame(details_card)
        details_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if full_data:
            # Parse data
            (id, patient_id, doctor_id, appointment_date, appointment_type, status, notes,
             created_at, updated_at, p_fname, p_lname, p_id, p_phone, p_email,
             d_fname, d_lname) = full_data
            
            # Format appointment date
            apt_datetime = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M:%S")
            
            # Create info grid
            info_items = [
                ("Appointment ID:", str(id)),
                ("Date:", apt_datetime.strftime("%Y-%m-%d")),
                ("Time:", apt_datetime.strftime("%H:%M")),
                ("Type:", appointment_type.title()),
                ("Status:", status.title()),
                ("Patient:", f"{p_fname} {p_lname} ({p_id})"),
                ("Patient Phone:", p_phone or "N/A"),
                ("Patient Email:", p_email or "N/A"),
                ("Doctor:", f"Dr. {d_fname} {d_lname}"),
                ("Created:", datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")),
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