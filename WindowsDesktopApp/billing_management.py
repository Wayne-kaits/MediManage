"""
Billing Management Module
Advanced billing system with modern UI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import sqlite3
from desktop_app import ModernWidget, ModernStyle

class BillingManagement:
    """Billing management interface"""
    
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        self.bills_data = []
        self.selected_bill = None
        
        self.create_interface()
        self.load_bills()
    
    def create_interface(self):
        """Create billing management interface"""
        # Title
        title_frame = ModernWidget.create_frame(self.parent)
        title_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ModernWidget.create_label(title_frame, "Billing Management", size="title")
        title_label.pack(side="left")
        
        # Action buttons
        btn_frame = ModernWidget.create_frame(title_frame)
        btn_frame.pack(side="right")
        
        add_btn = ModernWidget.create_button(btn_frame, "➕ Create Bill", self.add_bill, style="success")
        add_btn.pack(side="left", padx=(0, 10))
        
        edit_btn = ModernWidget.create_button(btn_frame, "✏️ Edit", self.edit_bill, style="primary")
        edit_btn.pack(side="left", padx=(0, 10))
        
        payment_btn = ModernWidget.create_button(btn_frame, "💰 Record Payment", self.record_payment, style="info")
        payment_btn.pack(side="left", padx=(0, 10))
        
        print_btn = ModernWidget.create_button(btn_frame, "🖨️ Print", self.print_bill, style="secondary")
        print_btn.pack(side="left", padx=(0, 10))
        
        view_btn = ModernWidget.create_button(btn_frame, "👁️ View Details", self.view_bill, style="info")
        view_btn.pack(side="left")
        
        # Filter frame
        filter_frame = ModernWidget.create_frame(self.parent)
        filter_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Status filter
        status_label = ModernWidget.create_label(filter_frame, "Status:")
        status_label.pack(side="left", padx=(0, 10))
        
        self.status_filter = ttk.Combobox(
            filter_frame,
            values=["All", "Pending", "Paid", "Partial", "Overdue"],
            state="readonly",
            width=12
        )
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=(0, 20))
        self.status_filter.bind("<<ComboboxSelected>>", self.on_status_filter)
        
        # Date range filter
        date_label = ModernWidget.create_label(filter_frame, "Date Range:")
        date_label.pack(side="left", padx=(0, 10))
        
        self.start_date = DateEntry(
            filter_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.start_date.pack(side="left", padx=(0, 5))
        
        to_label = ModernWidget.create_label(filter_frame, "to")
        to_label.pack(side="left", padx=5)
        
        self.end_date = DateEntry(
            filter_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd'
        )
        self.end_date.pack(side="left", padx=(5, 20))
        
        filter_btn = ModernWidget.create_button(filter_frame, "🔍 Filter", self.apply_date_filter, style="primary")
        filter_btn.pack(side="left", padx=(0, 20))
        
        # Search
        search_label = ModernWidget.create_label(filter_frame, "Search:")
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        search_entry = ModernWidget.create_entry(filter_frame, "Enter bill number or patient name...", width=30)
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.config(textvariable=self.search_var)
        
        refresh_btn = ModernWidget.create_button(filter_frame, "🔄 Refresh", self.load_bills, style="secondary")
        refresh_btn.pack(side="left")
        
        # Bills list
        list_frame = ModernWidget.create_card(self.parent, "Bills List")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create treeview
        self.create_bills_tree(list_frame)
    
    def create_bills_tree(self, parent):
        """Create bills treeview"""
        tree_frame = ModernWidget.create_frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Columns
        columns = ("ID", "Bill Number", "Patient", "Date", "Due Date", "Total", "Paid", "Balance", "Status")
        self.bills_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        column_widths = {"ID": 50, "Bill Number": 120, "Patient": 150, "Date": 100, "Due Date": 100,
                        "Total": 100, "Paid": 100, "Balance": 100, "Status": 100}
        
        for col in columns:
            self.bills_tree.heading(col, text=col, command=lambda c=col: self.sort_bills(c))
            self.bills_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.bills_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.bills_tree.xview)
        
        self.bills_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.bills_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Bind selection event
        self.bills_tree.bind("<<TreeviewSelect>>", self.on_bill_select)
        self.bills_tree.bind("<Double-1>", lambda e: self.view_bill())
    
    def load_bills(self):
        """Load bills from database"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.id, b.bill_number, b.total_amount, b.paid_amount, b.status,
                   b.bill_date, b.due_date, b.notes,
                   p.first_name, p.last_name, p.patient_id
            FROM bill b
            JOIN patient p ON b.patient_id = p.id
            ORDER BY b.created_at DESC
        ''')
        
        self.bills_data = cursor.fetchall()
        conn.close()
        
        self.populate_bills_tree()
    
    def populate_bills_tree(self, data=None):
        """Populate bills treeview"""
        # Clear existing items
        for item in self.bills_tree.get_children():
            self.bills_tree.delete(item)
        
        data = data or self.bills_data
        
        for bill in data:
            (id, bill_number, total_amount, paid_amount, status, bill_date, due_date, notes,
             p_fname, p_lname, patient_id) = bill
            
            # Calculate balance
            balance = total_amount - paid_amount
            
            # Format dates
            bill_date_str = datetime.strptime(bill_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            due_date_str = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            
            patient_name = f"{p_fname} {p_lname} ({patient_id})"
            
            # Color code by status
            tags = []
            if status == "paid":
                tags = ["paid"]
            elif status == "overdue":
                tags = ["overdue"]
            elif status == "partial":
                tags = ["partial"]
            elif datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S").date() < datetime.now().date() and status == "pending":
                tags = ["overdue"]
                # Update status in database
                self.update_overdue_status(id)
            
            self.bills_tree.insert("", "end", values=(
                id, bill_number, patient_name, bill_date_str, due_date_str,
                f"${total_amount:.2f}", f"${paid_amount:.2f}", f"${balance:.2f}", status.title()
            ), tags=tags)
        
        # Configure tags
        self.bills_tree.tag_configure("paid", background="#d4edda")
        self.bills_tree.tag_configure("overdue", background="#f8d7da")
        self.bills_tree.tag_configure("partial", background="#fff3cd")
    
    def update_overdue_status(self, bill_id):
        """Update bill status to overdue"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("UPDATE bill SET status = 'overdue' WHERE id = ?", (bill_id,))
            conn.commit()
            conn.close()
        except:
            pass
    
    def on_status_filter(self, event=None):
        """Handle status filter"""
        selected_status = self.status_filter.get().lower()
        
        if selected_status == "all":
            self.populate_bills_tree()
            return
        
        filtered_data = []
        for bill in self.bills_data:
            bill_status = bill[4].lower()
            # Check for overdue bills
            if selected_status == "overdue":
                due_date = datetime.strptime(bill[6], "%Y-%m-%d %H:%M:%S").date()
                if due_date < datetime.now().date() and bill_status == "pending":
                    bill_status = "overdue"
            
            if bill_status == selected_status:
                filtered_data.append(bill)
        
        self.populate_bills_tree(filtered_data)
    
    def apply_date_filter(self):
        """Apply date range filter"""
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        
        filtered_data = []
        for bill in self.bills_data:
            bill_date = datetime.strptime(bill[5], "%Y-%m-%d %H:%M:%S").date()
            if start_date <= bill_date <= end_date:
                filtered_data.append(bill)
        
        self.populate_bills_tree(filtered_data)
    
    def on_search(self, *args):
        """Handle search"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.populate_bills_tree()
            return
        
        filtered_data = []
        for bill in self.bills_data:
            bill_number = bill[1].lower()
            patient_name = f"{bill[8]} {bill[9]}".lower()
            patient_id = bill[10].lower()
            
            if (search_term in bill_number or 
                search_term in patient_name or 
                search_term in patient_id):
                filtered_data.append(bill)
        
        self.populate_bills_tree(filtered_data)
    
    def on_bill_select(self, event):
        """Handle bill selection"""
        selection = self.bills_tree.selection()
        if selection:
            item = self.bills_tree.item(selection[0])
            bill_id = item['values'][0]
            
            # Find selected bill data
            for bill in self.bills_data:
                if bill[0] == bill_id:
                    self.selected_bill = bill
                    break
    
    def sort_bills(self, column):
        """Sort bills by column"""
        # Implementation for sorting
        pass
    
    def add_bill(self):
        """Add new bill"""
        BillFormWindow(self, "Create Bill")
    
    def edit_bill(self):
        """Edit selected bill"""
        if not self.selected_bill:
            messagebox.showwarning("Warning", "Please select a bill to edit")
            return
        
        if self.selected_bill[4] == "paid":
            messagebox.showwarning("Warning", "Cannot edit paid bills")
            return
        
        BillFormWindow(self, "Edit Bill", self.selected_bill)
    
    def record_payment(self):
        """Record payment for selected bill"""
        if not self.selected_bill:
            messagebox.showwarning("Warning", "Please select a bill to record payment")
            return
        
        if self.selected_bill[4] == "paid":
            messagebox.showwarning("Warning", "Bill is already fully paid")
            return
        
        PaymentWindow(self, self.selected_bill)
    
    def print_bill(self):
        """Print selected bill"""
        if not self.selected_bill:
            messagebox.showwarning("Warning", "Please select a bill to print")
            return
        
        # Implementation for printing
        messagebox.showinfo("Print", "Print functionality would be implemented here")
    
    def view_bill(self):
        """View bill details"""
        if not self.selected_bill:
            messagebox.showwarning("Warning", "Please select a bill to view")
            return
        
        BillDetailsWindow(self.selected_bill, self.db)

class BillFormWindow:
    """Bill form window for add/edit"""
    
    def __init__(self, parent, title, bill_data=None):
        self.parent = parent
        self.bill_data = bill_data
        self.is_edit = bill_data is not None
        self.bill_items = []
        
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.geometry("700x800")
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
        x = (self.window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.window.winfo_screenheight() // 2) - (800 // 2)
        self.window.geometry(f"700x800+{x}+{y}")
    
    def create_form(self):
        """Create bill form"""
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form card
        form_card = ModernWidget.create_card(main_frame, "Bill Information")
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
        
        save_btn = ModernWidget.create_button(btn_frame, "💾 Save", self.save_bill, style="success")
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
        
        # Due date
        due_date_frame = ModernWidget.create_frame(parent)
        due_date_frame.pack(fill="x", pady=10)
        
        due_date_label = ModernWidget.create_label(due_date_frame, "Due Date *")
        due_date_label.pack(anchor="w")
        
        self.due_date_entry = DateEntry(
            due_date_frame,
            width=12,
            background=ModernStyle.BG_SECONDARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            date_pattern='yyyy-mm-dd',
            mindate=datetime.now().date()
        )
        self.due_date_entry.pack(anchor="w", pady=(5, 0))
        
        # Bill items section
        items_frame = ModernWidget.create_frame(parent)
        items_frame.pack(fill="x", pady=20)
        
        items_label = ModernWidget.create_label(items_frame, "Bill Items", size="large")
        items_label.pack(anchor="w", pady=(0, 10))
        
        # Items list
        self.items_tree_frame = ModernWidget.create_frame(items_frame)
        self.items_tree_frame.pack(fill="x", pady=(0, 10))
        
        self.create_items_tree()
        
        # Add item form
        add_item_frame = ModernWidget.create_frame(items_frame)
        add_item_frame.pack(fill="x", pady=10)
        
        # Description
        desc_frame = ModernWidget.create_frame(add_item_frame)
        desc_frame.pack(fill="x", pady=5)
        
        desc_label = ModernWidget.create_label(desc_frame, "Description")
        desc_label.pack(side="left", padx=(0, 10))
        
        self.desc_var = tk.StringVar()
        desc_entry = ModernWidget.create_entry(desc_frame, width=30)
        desc_entry.pack(side="left", padx=(0, 10))
        desc_entry.config(textvariable=self.desc_var)
        
        # Quantity
        qty_label = ModernWidget.create_label(desc_frame, "Qty")
        qty_label.pack(side="left", padx=(10, 5))
        
        self.qty_var = tk.StringVar(value="1")
        qty_entry = ModernWidget.create_entry(desc_frame, width=5)
        qty_entry.pack(side="left", padx=(0, 10))
        qty_entry.config(textvariable=self.qty_var)
        
        # Unit price
        price_label = ModernWidget.create_label(desc_frame, "Price")
        price_label.pack(side="left", padx=(10, 5))
        
        self.price_var = tk.StringVar()
        price_entry = ModernWidget.create_entry(desc_frame, width=10)
        price_entry.pack(side="left", padx=(0, 10))
        price_entry.config(textvariable=self.price_var)
        
        # Add button
        add_item_btn = ModernWidget.create_button(desc_frame, "➕ Add Item", self.add_item, style="success")
        add_item_btn.pack(side="left", padx=10)
        
        # Total section
        total_frame = ModernWidget.create_frame(parent)
        total_frame.pack(fill="x", pady=20)
        
        self.total_label = ModernWidget.create_label(total_frame, "Total Amount: $0.00", size="large")
        self.total_label.pack(anchor="e")
        
        # Notes
        notes_frame = ModernWidget.create_frame(parent)
        notes_frame.pack(fill="x", pady=10)
        
        notes_label = ModernWidget.create_label(notes_frame, "Notes")
        notes_label.pack(anchor="w")
        
        self.notes_text = ModernWidget.create_text(notes_frame, height=4)
        self.notes_text.pack(fill="x", pady=(5, 0))
    
    def create_items_tree(self):
        """Create bill items treeview"""
        columns = ("Description", "Quantity", "Unit Price", "Total")
        self.items_tree = ttk.Treeview(self.items_tree_frame, columns=columns, show="headings", height=6)
        
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=150)
        
        self.items_tree.pack(fill="x")
        
        # Context menu for removing items
        self.items_tree.bind("<Button-3>", self.show_item_context_menu)
    
    def show_item_context_menu(self, event):
        """Show context menu for items"""
        selection = self.items_tree.selection()
        if selection:
            menu = tk.Menu(self.window, tearoff=0)
            menu.add_command(label="Remove Item", command=self.remove_selected_item)
            menu.tk_popup(event.x_root, event.y_root)
    
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
    
    def add_item(self):
        """Add item to bill"""
        description = self.desc_var.get().strip()
        quantity_str = self.qty_var.get().strip()
        price_str = self.price_var.get().strip()
        
        if not description:
            messagebox.showerror("Error", "Please enter item description")
            return
        
        try:
            quantity = int(quantity_str)
            unit_price = float(price_str)
            
            if quantity <= 0 or unit_price < 0:
                raise ValueError()
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity and price")
            return
        
        total_price = quantity * unit_price
        
        # Add to items list
        item = {
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price
        }
        
        self.bill_items.append(item)
        
        # Add to treeview
        self.items_tree.insert("", "end", values=(
            description, quantity, f"${unit_price:.2f}", f"${total_price:.2f}"
        ))
        
        # Clear form
        self.desc_var.set("")
        self.qty_var.set("1")
        self.price_var.set("")
        
        # Update total
        self.update_total()
    
    def remove_selected_item(self):
        """Remove selected item from bill"""
        selection = self.items_tree.selection()
        if selection:
            item_index = self.items_tree.index(selection[0])
            
            # Remove from list
            del self.bill_items[item_index]
            
            # Remove from treeview
            self.items_tree.delete(selection[0])
            
            # Update total
            self.update_total()
    
    def update_total(self):
        """Update total amount"""
        total = sum(item['total_price'] for item in self.bill_items)
        self.total_label.config(text=f"Total Amount: ${total:.2f}")
    
    def populate_form(self):
        """Populate form with bill data"""
        if not self.bill_data:
            return
        
        # Get full bill data
        conn = self.parent.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.*, p.first_name, p.last_name, p.patient_id
            FROM bill b
            JOIN patient p ON b.patient_id = p.id
            WHERE b.id = ?
        ''', (self.bill_data[0],))
        
        full_data = cursor.fetchone()
        
        # Get bill items
        cursor.execute('''
            SELECT description, quantity, unit_price, total_price
            FROM bill_item
            WHERE bill_id = ?
        ''', (self.bill_data[0],))
        
        items_data = cursor.fetchall()
        conn.close()
        
        if full_data:
            # Set patient
            patient_display = f"{full_data[12]} {full_data[13]} ({full_data[14]})"
            self.patient_var.set(patient_display)
            
            # Set due date
            due_date = datetime.strptime(full_data[7], "%Y-%m-%d %H:%M:%S").date()
            self.due_date_entry.set_date(due_date)
            
            # Set notes
            if full_data[8]:
                self.notes_text.insert("1.0", full_data[8])
            
            # Load items
            for item_data in items_data:
                description, quantity, unit_price, total_price = item_data
                
                item = {
                    'description': description,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_price': total_price
                }
                
                self.bill_items.append(item)
                
                self.items_tree.insert("", "end", values=(
                    description, quantity, f"${unit_price:.2f}", f"${total_price:.2f}"
                ))
            
            self.update_total()
    
    def save_bill(self):
        """Save bill data"""
        # Validate required fields
        if not self.patient_var.get():
            messagebox.showerror("Error", "Please select a patient")
            return
        
        if not self.bill_items:
            messagebox.showerror("Error", "Please add at least one item to the bill")
            return
        
        try:
            patient_id = self.patients_data[self.patient_var.get()]
            due_date = self.due_date_entry.get_date()
            total_amount = sum(item['total_price'] for item in self.bill_items)
            notes = self.notes_text.get("1.0", tk.END).strip() or None
            
            conn = self.parent.db.get_connection()
            cursor = conn.cursor()
            
            if self.is_edit:
                # Update existing bill
                cursor.execute('''
                    UPDATE bill SET
                        patient_id = ?, total_amount = ?, due_date = ?, notes = ?
                    WHERE id = ?
                ''', (patient_id, total_amount, due_date.strftime('%Y-%m-%d %H:%M:%S'), 
                      notes, self.bill_data[0]))
                
                # Delete existing items
                cursor.execute("DELETE FROM bill_item WHERE bill_id = ?", (self.bill_data[0],))
                
                bill_id = self.bill_data[0]
                message = "Bill updated successfully"
            else:
                # Generate bill number
                cursor.execute("SELECT COUNT(*) FROM bill")
                count = cursor.fetchone()[0]
                bill_number = f"B{count + 1:06d}"
                
                # Insert new bill
                cursor.execute('''
                    INSERT INTO bill (
                        bill_number, patient_id, total_amount, due_date, notes
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (bill_number, patient_id, total_amount, 
                      due_date.strftime('%Y-%m-%d %H:%M:%S'), notes))
                
                bill_id = cursor.lastrowid
                message = "Bill created successfully"
            
            # Insert bill items
            for item in self.bill_items:
                cursor.execute('''
                    INSERT INTO bill_item (
                        bill_id, description, quantity, unit_price, total_price
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (bill_id, item['description'], item['quantity'], 
                      item['unit_price'], item['total_price']))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", message)
            self.parent.load_bills()
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {str(e)}")

class PaymentWindow:
    """Payment recording window"""
    
    def __init__(self, parent, bill_data):
        self.parent = parent
        self.bill_data = bill_data
        
        self.window = tk.Toplevel()
        self.window.title("Record Payment")
        self.window.geometry("400x300")
        self.window.configure(bg=ModernStyle.BG_PRIMARY)
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Make modal
        self.window.transient(parent.parent)
        self.window.grab_set()
        
        self.create_form()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (300 // 2)
        self.window.geometry(f"400x300+{x}+{y}")
    
    def create_form(self):
        """Create payment form"""
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form card
        form_card = ModernWidget.create_card(main_frame, "Record Payment")
        form_card.pack(fill="both", expand=True)
        
        form_frame = ModernWidget.create_frame(form_card)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Bill info
        total_amount = self.bill_data[2]
        paid_amount = self.bill_data[3]
        balance = total_amount - paid_amount
        
        info_frame = ModernWidget.create_frame(form_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        total_label = ModernWidget.create_label(info_frame, f"Total Amount: ${total_amount:.2f}")
        total_label.pack(anchor="w")
        
        paid_label = ModernWidget.create_label(info_frame, f"Paid Amount: ${paid_amount:.2f}")
        paid_label.pack(anchor="w")
        
        balance_label = ModernWidget.create_label(info_frame, f"Balance: ${balance:.2f}", style="danger")
        balance_label.pack(anchor="w")
        
        # Payment amount
        amount_frame = ModernWidget.create_frame(form_frame)
        amount_frame.pack(fill="x", pady=10)
        
        amount_label = ModernWidget.create_label(amount_frame, "Payment Amount *")
        amount_label.pack(anchor="w")
        
        self.amount_var = tk.StringVar(value=str(balance))
        amount_entry = ModernWidget.create_entry(amount_frame, width=20)
        amount_entry.pack(fill="x", pady=(5, 0))
        amount_entry.config(textvariable=self.amount_var)
        
        # Payment method
        method_frame = ModernWidget.create_frame(form_frame)
        method_frame.pack(fill="x", pady=10)
        
        method_label = ModernWidget.create_label(method_frame, "Payment Method")
        method_label.pack(anchor="w")
        
        self.method_var = tk.StringVar(value="Cash")
        method_combo = ttk.Combobox(
            method_frame,
            textvariable=self.method_var,
            values=["Cash", "Credit Card", "Debit Card", "Check", "Bank Transfer"],
            state="readonly"
        )
        method_combo.pack(fill="x", pady=(5, 0))
        
        # Buttons
        btn_frame = ModernWidget.create_frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        record_btn = ModernWidget.create_button(btn_frame, "💰 Record Payment", self.record_payment, style="success")
        record_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = ModernWidget.create_button(btn_frame, "❌ Cancel", self.window.destroy, style="secondary")
        cancel_btn.pack(side="right")
    
    def record_payment(self):
        """Record the payment"""
        try:
            payment_amount = float(self.amount_var.get())
            
            if payment_amount <= 0:
                messagebox.showerror("Error", "Payment amount must be greater than 0")
                return
            
            total_amount = self.bill_data[2]
            current_paid = self.bill_data[3]
            balance = total_amount - current_paid
            
            if payment_amount > balance:
                messagebox.showerror("Error", f"Payment amount cannot exceed balance of ${balance:.2f}")
                return
            
            new_paid_amount = current_paid + payment_amount
            
            # Determine new status
            if new_paid_amount >= total_amount:
                new_status = "paid"
            elif new_paid_amount > 0:
                new_status = "partial"
            else:
                new_status = "pending"
            
            # Update database
            conn = self.parent.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE bill SET paid_amount = ?, status = ?
                WHERE id = ?
            ''', (new_paid_amount, new_status, self.bill_data[0]))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Payment of ${payment_amount:.2f} recorded successfully")
            self.parent.load_bills()
            self.window.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid payment amount")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record payment: {str(e)}")

class BillDetailsWindow:
    """Bill details view window"""
    
    def __init__(self, bill_data, db):
        self.bill_data = bill_data
        self.db = db
        
        self.window = tk.Toplevel()
        self.window.title("Bill Details")
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
        """Create bill details view"""
        # Get full bill data
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.*, p.first_name, p.last_name, p.patient_id, p.phone, p.email
            FROM bill b
            JOIN patient p ON b.patient_id = p.id
            WHERE b.id = ?
        ''', (self.bill_data[0],))
        
        full_data = cursor.fetchone()
        
        # Get bill items
        cursor.execute('''
            SELECT description, quantity, unit_price, total_price
            FROM bill_item
            WHERE bill_id = ?
        ''', (self.bill_data[0],))
        
        items_data = cursor.fetchall()
        conn.close()
        
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ModernWidget.create_frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ModernWidget.create_label(
            title_frame, 
            f"Bill Details - {full_data[1]}", 
            size="title"
        )
        title_label.pack(side="left")
        
        close_btn = ModernWidget.create_button(title_frame, "❌ Close", self.window.destroy, style="secondary")
        close_btn.pack(side="right")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Bill info tab
        info_tab = ModernWidget.create_frame(notebook)
        notebook.add(info_tab, text="Bill Information")
        
        # Items tab
        items_tab = ModernWidget.create_frame(notebook)
        notebook.add(items_tab, text="Bill Items")
        
        # Populate tabs
        self.populate_info_tab(info_tab, full_data)
        self.populate_items_tab(items_tab, items_data)
    
    def populate_info_tab(self, parent, data):
        """Populate bill information tab"""
        info_frame = ModernWidget.create_card(parent, "Bill Information")
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        details_frame = ModernWidget.create_frame(info_frame)
        details_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Parse data
        (id, bill_number, patient_id, appointment_id, total_amount, paid_amount, status,
         bill_date, due_date, notes, created_at, p_fname, p_lname, p_id, p_phone, p_email) = data
        
        balance = total_amount - paid_amount
        
        # Create info grid
        info_items = [
            ("Bill Number:", bill_number),
            ("Patient:", f"{p_fname} {p_lname} ({p_id})"),
            ("Patient Phone:", p_phone or "N/A"),
            ("Patient Email:", p_email or "N/A"),
            ("Bill Date:", datetime.strptime(bill_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")),
            ("Due Date:", datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")),
            ("Total Amount:", f"${total_amount:.2f}"),
            ("Paid Amount:", f"${paid_amount:.2f}"),
            ("Balance:", f"${balance:.2f}"),
            ("Status:", status.title()),
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
    
    def populate_items_tab(self, parent, items_data):
        """Populate bill items tab"""
        items_frame = ModernWidget.create_card(parent, "Bill Items")
        items_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tree_frame = ModernWidget.create_frame(items_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create treeview
        columns = ("Description", "Quantity", "Unit Price", "Total Price")
        items_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=150)
        
        # Populate items
        total = 0
        for item in items_data:
            description, quantity, unit_price, total_price = item
            items_tree.insert("", "end", values=(
                description, quantity, f"${unit_price:.2f}", f"${total_price:.2f}"
            ))
            total += total_price
        
        items_tree.pack(fill="both", expand=True)
        
        # Total
        total_frame = ModernWidget.create_frame(items_frame)
        total_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        total_label = ModernWidget.create_label(total_frame, f"Total: ${total:.2f}", size="large")
        total_label.pack(anchor="e")