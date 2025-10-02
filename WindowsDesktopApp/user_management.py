"""
User Management Module
Advanced user management with role-based access control
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
import hashlib
from desktop_app import ModernWidget, ModernStyle

class UserManagement:
    """User management interface (Admin only)"""
    
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        self.users_data = []
        self.selected_user = None
        
        # Check if user is admin
        if current_user['role'] != 'admin':
            self.show_access_denied()
            return
        
        self.create_interface()
        self.load_users()
    
    def show_access_denied(self):
        """Show access denied message"""
        access_frame = ModernWidget.create_frame(self.parent)
        access_frame.pack(fill="both", expand=True)
        
        denied_label = ModernWidget.create_label(
            access_frame, 
            "🚫 Access Denied", 
            size="title",
            style="danger"
        )
        denied_label.pack(expand=True)
        
        message_label = ModernWidget.create_label(
            access_frame, 
            "You need administrator privileges to access user management.",
            style="secondary"
        )
        message_label.pack(expand=True)
    
    def create_interface(self):
        """Create user management interface"""
        # Title
        title_frame = ModernWidget.create_frame(self.parent)
        title_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ModernWidget.create_label(title_frame, "User Management", size="title")
        title_label.pack(side="left")
        
        # Action buttons
        btn_frame = ModernWidget.create_frame(title_frame)
        btn_frame.pack(side="right")
        
        add_btn = ModernWidget.create_button(btn_frame, "➕ Add User", self.add_user, style="success")
        add_btn.pack(side="left", padx=(0, 10))
        
        edit_btn = ModernWidget.create_button(btn_frame, "✏️ Edit", self.edit_user, style="primary")
        edit_btn.pack(side="left", padx=(0, 10))
        
        reset_btn = ModernWidget.create_button(btn_frame, "🔑 Reset Password", self.reset_password, style="warning")
        reset_btn.pack(side="left", padx=(0, 10))
        
        toggle_btn = ModernWidget.create_button(btn_frame, "🔄 Toggle Status", self.toggle_status, style="info")
        toggle_btn.pack(side="left", padx=(0, 10))
        
        view_btn = ModernWidget.create_button(btn_frame, "👁️ View Details", self.view_user, style="info")
        view_btn.pack(side="left")
        
        # Filter frame
        filter_frame = ModernWidget.create_frame(self.parent)
        filter_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Role filter
        role_label = ModernWidget.create_label(filter_frame, "Role:")
        role_label.pack(side="left", padx=(0, 10))
        
        self.role_filter = ttk.Combobox(
            filter_frame,
            values=["All", "Admin", "Doctor", "Staff"],
            state="readonly",
            width=12
        )
        self.role_filter.set("All")
        self.role_filter.pack(side="left", padx=(0, 20))
        self.role_filter.bind("<<ComboboxSelected>>", self.on_role_filter)
        
        # Status filter
        status_label = ModernWidget.create_label(filter_frame, "Status:")
        status_label.pack(side="left", padx=(0, 10))
        
        self.status_filter = ttk.Combobox(
            filter_frame,
            values=["All", "Active", "Inactive"],
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
        search_entry = ModernWidget.create_entry(filter_frame, "Enter username or name...", width=30)
        search_entry.pack(side="left", padx=(0, 10))
        search_entry.config(textvariable=self.search_var)
        
        refresh_btn = ModernWidget.create_button(filter_frame, "🔄 Refresh", self.load_users, style="secondary")
        refresh_btn.pack(side="left")
        
        # Users list
        list_frame = ModernWidget.create_card(self.parent, "Users List")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create treeview
        self.create_users_tree(list_frame)
    
    def create_users_tree(self, parent):
        """Create users treeview"""
        tree_frame = ModernWidget.create_frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Columns
        columns = ("ID", "Username", "Name", "Email", "Role", "Status", "Created", "Last Login")
        self.users_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        column_widths = {"ID": 50, "Username": 120, "Name": 150, "Email": 180, "Role": 80,
                        "Status": 80, "Created": 100, "Last Login": 120}
        
        for col in columns:
            self.users_tree.heading(col, text=col, command=lambda c=col: self.sort_users(c))
            self.users_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.users_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.users_tree.xview)
        
        self.users_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.users_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Bind selection event
        self.users_tree.bind("<<TreeviewSelect>>", self.on_user_select)
        self.users_tree.bind("<Double-1>", lambda e: self.view_user())
    
    def load_users(self):
        """Load users from database"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, role, first_name, last_name, 
                   created_at, is_active
            FROM user
            ORDER BY created_at DESC
        ''')
        
        self.users_data = cursor.fetchall()
        conn.close()
        
        self.populate_users_tree()
    
    def populate_users_tree(self, data=None):
        """Populate users treeview"""
        # Clear existing items
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        data = data or self.users_data
        
        for user in data:
            (id, username, email, role, first_name, last_name, created_at, is_active) = user
            
            name = f"{first_name} {last_name}"
            status = "Active" if is_active else "Inactive"
            created_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            
            # Color code by status
            tags = []
            if not is_active:
                tags = ["inactive"]
            elif role == "admin":
                tags = ["admin"]
            
            self.users_tree.insert("", "end", values=(
                id, username, name, email, role.title(), status, created_date, "N/A"
            ), tags=tags)
        
        # Configure tags
        self.users_tree.tag_configure("inactive", background="#f8d7da")
        self.users_tree.tag_configure("admin", background="#d1ecf1")
    
    def on_role_filter(self, event=None):
        """Handle role filter"""
        selected_role = self.role_filter.get().lower()
        
        if selected_role == "all":
            self.populate_users_tree()
            return
        
        filtered_data = []
        for user in self.users_data:
            if user[3].lower() == selected_role:
                filtered_data.append(user)
        
        self.populate_users_tree(filtered_data)
    
    def on_status_filter(self, event=None):
        """Handle status filter"""
        selected_status = self.status_filter.get().lower()
        
        if selected_status == "all":
            self.populate_users_tree()
            return
        
        filtered_data = []
        for user in self.users_data:
            is_active = user[7]
            if (selected_status == "active" and is_active) or (selected_status == "inactive" and not is_active):
                filtered_data.append(user)
        
        self.populate_users_tree(filtered_data)
    
    def on_search(self, *args):
        """Handle search"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.populate_users_tree()
            return
        
        filtered_data = []
        for user in self.users_data:
            username = user[1].lower()
            name = f"{user[4]} {user[5]}".lower()
            email = user[2].lower()
            
            if (search_term in username or 
                search_term in name or 
                search_term in email):
                filtered_data.append(user)
        
        self.populate_users_tree(filtered_data)
    
    def on_user_select(self, event):
        """Handle user selection"""
        selection = self.users_tree.selection()
        if selection:
            item = self.users_tree.item(selection[0])
            user_id = item['values'][0]
            
            # Find selected user data
            for user in self.users_data:
                if user[0] == user_id:
                    self.selected_user = user
                    break
    
    def sort_users(self, column):
        """Sort users by column"""
        # Implementation for sorting
        pass
    
    def add_user(self):
        """Add new user"""
        UserFormWindow(self, "Add User")
    
    def edit_user(self):
        """Edit selected user"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a user to edit")
            return
        
        UserFormWindow(self, "Edit User", self.selected_user)
    
    def reset_password(self):
        """Reset password for selected user"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a user to reset password")
            return
        
        username = self.selected_user[1]
        result = messagebox.askyesno(
            "Confirm Password Reset", 
            f"Reset password for user '{username}' to default password 'password123'?"
        )
        
        if result:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                # Hash default password
                default_password = "password123"
                password_hash = hashlib.sha256(default_password.encode()).hexdigest()
                
                cursor.execute('''
                    UPDATE user SET password_hash = ?
                    WHERE id = ?
                ''', (password_hash, self.selected_user[0]))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"Password reset for user '{username}'\nNew password: {default_password}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset password: {str(e)}")
    
    def toggle_status(self):
        """Toggle user active status"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a user to toggle status")
            return
        
        username = self.selected_user[1]
        current_status = "Active" if self.selected_user[7] else "Inactive"
        new_status = "Inactive" if self.selected_user[7] else "Active"
        
        # Prevent deactivating the current user
        if self.selected_user[0] == self.current_user['id'] and self.selected_user[7]:
            messagebox.showwarning("Warning", "You cannot deactivate your own account")
            return
        
        result = messagebox.askyesno(
            "Confirm Status Change", 
            f"Change status for user '{username}' from {current_status} to {new_status}?"
        )
        
        if result:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                new_is_active = not self.selected_user[7]
                
                cursor.execute('''
                    UPDATE user SET is_active = ?
                    WHERE id = ?
                ''', (new_is_active, self.selected_user[0]))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"User status changed to {new_status}")
                self.load_users()
                self.selected_user = None
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change user status: {str(e)}")
    
    def view_user(self):
        """View user details"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a user to view")
            return
        
        UserDetailsWindow(self.selected_user, self.db)

class UserFormWindow:
    """User form window for add/edit"""
    
    def __init__(self, parent, title, user_data=None):
        self.parent = parent
        self.user_data = user_data
        self.is_edit = user_data is not None
        
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
        """Create user form"""
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form card
        form_card = ModernWidget.create_card(main_frame, "User Information")
        form_card.pack(fill="both", expand=True)
        
        # Form container
        form_frame = ModernWidget.create_frame(form_card)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Username
        username_frame = ModernWidget.create_frame(form_frame)
        username_frame.pack(fill="x", pady=10)
        
        username_label = ModernWidget.create_label(username_frame, "Username *")
        username_label.pack(anchor="w")
        
        self.username_var = tk.StringVar()
        username_entry = ModernWidget.create_entry(username_frame, width=40)
        username_entry.pack(fill="x", pady=(5, 0))
        username_entry.config(textvariable=self.username_var)
        
        # Email
        email_frame = ModernWidget.create_frame(form_frame)
        email_frame.pack(fill="x", pady=10)
        
        email_label = ModernWidget.create_label(email_frame, "Email *")
        email_label.pack(anchor="w")
        
        self.email_var = tk.StringVar()
        email_entry = ModernWidget.create_entry(email_frame, width=40)
        email_entry.pack(fill="x", pady=(5, 0))
        email_entry.config(textvariable=self.email_var)
        
        # First Name
        fname_frame = ModernWidget.create_frame(form_frame)
        fname_frame.pack(fill="x", pady=10)
        
        fname_label = ModernWidget.create_label(fname_frame, "First Name *")
        fname_label.pack(anchor="w")
        
        self.fname_var = tk.StringVar()
        fname_entry = ModernWidget.create_entry(fname_frame, width=40)
        fname_entry.pack(fill="x", pady=(5, 0))
        fname_entry.config(textvariable=self.fname_var)
        
        # Last Name
        lname_frame = ModernWidget.create_frame(form_frame)
        lname_frame.pack(fill="x", pady=10)
        
        lname_label = ModernWidget.create_label(lname_frame, "Last Name *")
        lname_label.pack(anchor="w")
        
        self.lname_var = tk.StringVar()
        lname_entry = ModernWidget.create_entry(lname_frame, width=40)
        lname_entry.pack(fill="x", pady=(5, 0))
        lname_entry.config(textvariable=self.lname_var)
        
        # Role
        role_frame = ModernWidget.create_frame(form_frame)
        role_frame.pack(fill="x", pady=10)
        
        role_label = ModernWidget.create_label(role_frame, "Role *")
        role_label.pack(anchor="w")
        
        self.role_var = tk.StringVar(value="staff")
        role_combo = ttk.Combobox(
            role_frame,
            textvariable=self.role_var,
            values=["admin", "doctor", "staff"],
            state="readonly",
            width=40
        )
        role_combo.pack(fill="x", pady=(5, 0))
        
        # Password (only for new users)
        if not self.is_edit:
            password_frame = ModernWidget.create_frame(form_frame)
            password_frame.pack(fill="x", pady=10)
            
            password_label = ModernWidget.create_label(password_frame, "Password *")
            password_label.pack(anchor="w")
            
            self.password_var = tk.StringVar()
            password_entry = tk.Entry(
                password_frame,
                show="*",
                bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.TEXT_PRIMARY,
                font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
                relief="flat",
                borderwidth=1,
                highlightthickness=1,
                highlightcolor=ModernStyle.BTN_PRIMARY,
                highlightbackground=ModernStyle.BORDER_COLOR,
                insertbackground=ModernStyle.TEXT_PRIMARY,
                textvariable=self.password_var
            )
            password_entry.pack(fill="x", pady=(5, 0))
            
            # Confirm Password
            confirm_frame = ModernWidget.create_frame(form_frame)
            confirm_frame.pack(fill="x", pady=10)
            
            confirm_label = ModernWidget.create_label(confirm_frame, "Confirm Password *")
            confirm_label.pack(anchor="w")
            
            self.confirm_var = tk.StringVar()
            confirm_entry = tk.Entry(
                confirm_frame,
                show="*",
                bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.TEXT_PRIMARY,
                font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
                relief="flat",
                borderwidth=1,
                highlightthickness=1,
                highlightcolor=ModernStyle.BTN_PRIMARY,
                highlightbackground=ModernStyle.BORDER_COLOR,
                insertbackground=ModernStyle.TEXT_PRIMARY,
                textvariable=self.confirm_var
            )
            confirm_entry.pack(fill="x", pady=(5, 0))
        
        # Status (only for edit)
        if self.is_edit:
            status_frame = ModernWidget.create_frame(form_frame)
            status_frame.pack(fill="x", pady=10)
            
            status_label = ModernWidget.create_label(status_frame, "Status")
            status_label.pack(anchor="w")
            
            self.status_var = tk.BooleanVar(value=True)
            status_check = tk.Checkbutton(
                status_frame,
                text="Active",
                variable=self.status_var,
                bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.TEXT_PRIMARY,
                selectcolor=ModernStyle.BG_DARK,
                activebackground=ModernStyle.BG_SECONDARY,
                activeforeground=ModernStyle.TEXT_PRIMARY
            )
            status_check.pack(anchor="w", pady=(5, 0))
        
        # Buttons
        btn_frame = ModernWidget.create_frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        save_btn = ModernWidget.create_button(btn_frame, "💾 Save", self.save_user, style="success")
        save_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = ModernWidget.create_button(btn_frame, "❌ Cancel", self.window.destroy, style="secondary")
        cancel_btn.pack(side="right")
    
    def populate_form(self):
        """Populate form with user data"""
        if not self.user_data:
            return
        
        (id, username, email, role, first_name, last_name, created_at, is_active) = self.user_data
        
        self.username_var.set(username)
        self.email_var.set(email)
        self.fname_var.set(first_name)
        self.lname_var.set(last_name)
        self.role_var.set(role)
        
        if self.is_edit:
            self.status_var.set(is_active)
    
    def save_user(self):
        """Save user data"""
        # Validate required fields
        if not self.username_var.get().strip():
            messagebox.showerror("Error", "Username is required")
            return
        
        if not self.email_var.get().strip():
            messagebox.showerror("Error", "Email is required")
            return
        
        if not self.fname_var.get().strip():
            messagebox.showerror("Error", "First name is required")
            return
        
        if not self.lname_var.get().strip():
            messagebox.showerror("Error", "Last name is required")
            return
        
        if not self.is_edit:
            if not self.password_var.get():
                messagebox.showerror("Error", "Password is required")
                return
            
            if self.password_var.get() != self.confirm_var.get():
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            if len(self.password_var.get()) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters long")
                return
        
        try:
            conn = self.parent.db.get_connection()
            cursor = conn.cursor()
            
            username = self.username_var.get().strip()
            email = self.email_var.get().strip()
            
            if self.is_edit:
                # Check for duplicates (excluding current user)
                cursor.execute('''
                    SELECT id FROM user 
                    WHERE (username = ? OR email = ?) AND id != ?
                ''', (username, email, self.user_data[0]))
                
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username or email already exists")
                    return
                
                # Update existing user
                cursor.execute('''
                    UPDATE user SET
                        username = ?, email = ?, role = ?, first_name = ?, 
                        last_name = ?, is_active = ?
                    WHERE id = ?
                ''', (
                    username, email, self.role_var.get(), self.fname_var.get().strip(),
                    self.lname_var.get().strip(), self.status_var.get(), self.user_data[0]
                ))
                
                message = "User updated successfully"
            else:
                # Check for duplicates
                cursor.execute('''
                    SELECT id FROM user 
                    WHERE username = ? OR email = ?
                ''', (username, email))
                
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username or email already exists")
                    return
                
                # Hash password
                password_hash = hashlib.sha256(self.password_var.get().encode()).hexdigest()
                
                # Insert new user
                cursor.execute('''
                    INSERT INTO user (
                        username, email, password_hash, role, first_name, last_name
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    username, email, password_hash, self.role_var.get(),
                    self.fname_var.get().strip(), self.lname_var.get().strip()
                ))
                
                message = "User created successfully"
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", message)
            self.parent.load_users()
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user: {str(e)}")

class UserDetailsWindow:
    """User details view window"""
    
    def __init__(self, user_data, db):
        self.user_data = user_data
        self.db = db
        
        self.window = tk.Toplevel()
        self.window.title("User Details")
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
        """Create user details view"""
        # Main container
        main_frame = ModernWidget.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ModernWidget.create_frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ModernWidget.create_label(
            title_frame, 
            f"User Details - {self.user_data[1]}", 
            size="title"
        )
        title_label.pack(side="left")
        
        close_btn = ModernWidget.create_button(title_frame, "❌ Close", self.window.destroy, style="secondary")
        close_btn.pack(side="right")
        
        # Details card
        details_card = ModernWidget.create_card(main_frame, "User Information")
        details_card.pack(fill="both", expand=True)
        
        details_frame = ModernWidget.create_frame(details_card)
        details_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Parse data
        (id, username, email, role, first_name, last_name, created_at, is_active) = self.user_data
        
        # Get additional statistics
        stats = self.get_user_stats(id)
        
        # Create info grid
        info_items = [
            ("User ID:", str(id)),
            ("Username:", username),
            ("Full Name:", f"{first_name} {last_name}"),
            ("Email:", email),
            ("Role:", role.title()),
            ("Status:", "Active" if is_active else "Inactive"),
            ("Created:", datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")),
            ("Appointments Scheduled:", str(stats['appointments']) if role in ['doctor', 'admin'] else "N/A"),
            ("Lab Tests Ordered:", str(stats['lab_tests']) if role in ['doctor', 'admin'] else "N/A"),
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
        
        # Activity summary
        if role in ['doctor', 'admin'] and (stats['appointments'] > 0 or stats['lab_tests'] > 0):
            activity_frame = ModernWidget.create_frame(details_frame)
            activity_frame.grid(row=len(info_items)//2 + 1, column=0, columnspan=2, sticky="ew", padx=10, pady=20)
            
            activity_label = ModernWidget.create_label(activity_frame, "Recent Activity:", style="secondary", size="large")
            activity_label.pack(anchor="w", pady=(0, 10))
            
            # Recent appointments
            if stats['appointments'] > 0:
                recent_appointments = self.get_recent_appointments(id)
                if recent_appointments:
                    apt_label = ModernWidget.create_label(activity_frame, "Recent Appointments:", style="secondary")
                    apt_label.pack(anchor="w")
                    
                    for apt in recent_appointments[:3]:  # Show last 3
                        apt_text = f"• {apt[0]} - {apt[1]} ({apt[2]})"
                        apt_item = ModernWidget.create_label(activity_frame, apt_text, style="primary")
                        apt_item.pack(anchor="w", padx=20)
            
            # Recent lab tests
            if stats['lab_tests'] > 0:
                recent_tests = self.get_recent_lab_tests(id)
                if recent_tests:
                    test_label = ModernWidget.create_label(activity_frame, "Recent Lab Tests:", style="secondary")
                    test_label.pack(anchor="w", pady=(10, 0))
                    
                    for test in recent_tests[:3]:  # Show last 3
                        test_text = f"• {test[0]} - {test[1]} ({test[2]})"
                        test_item = ModernWidget.create_label(activity_frame, test_text, style="primary")
                        test_item.pack(anchor="w", padx=20)
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Appointments scheduled (for doctors)
        cursor.execute("SELECT COUNT(*) FROM appointment WHERE doctor_id = ?", (user_id,))
        stats['appointments'] = cursor.fetchone()[0]
        
        # Lab tests ordered (for doctors)
        cursor.execute("SELECT COUNT(*) FROM lab_test WHERE ordered_by = ?", (user_id,))
        stats['lab_tests'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def get_recent_appointments(self, user_id):
        """Get recent appointments for user"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.first_name || ' ' || p.last_name as patient_name,
                   a.appointment_type,
                   DATE(a.appointment_date) as date
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            WHERE a.doctor_id = ?
            ORDER BY a.appointment_date DESC
            LIMIT 5
        ''', (user_id,))
        
        appointments = cursor.fetchall()
        conn.close()
        return appointments
    
    def get_recent_lab_tests(self, user_id):
        """Get recent lab tests ordered by user"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.first_name || ' ' || p.last_name as patient_name,
                   lt.test_name,
                   DATE(lt.ordered_date) as date
            FROM lab_test lt
            JOIN patient p ON lt.patient_id = p.id
            WHERE lt.ordered_by = ?
            ORDER BY lt.ordered_date DESC
            LIMIT 5
        ''', (user_id,))
        
        tests = cursor.fetchall()
        conn.close()
        return tests