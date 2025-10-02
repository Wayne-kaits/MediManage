"""
Hospital Management System - Professional Setup Installer
Publisher: Kaitsnet IT Solutions
Advanced Windows Desktop Application Setup
"""

import os
import sys
import subprocess
import shutil
import winreg
import json
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class SetupInstaller:
    """Professional setup installer for Hospital Management System"""
    
    def __init__(self):
        self.app_name = "Hospital Management System"
        self.app_version = "1.0.0"
        self.publisher = "Kaitsnet IT Solutions"
        self.app_id = "HospitalManagementSystem"
        self.install_dir = None
        self.create_shortcuts = True
        self.agreement_accepted = False
        
        # Setup window
        self.root = tk.Tk()
        self.root.title(f"{self.app_name} Setup")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Center window
        self.center_window()
        
        # Setup variables
        self.current_step = 0
        self.steps = [
            "Welcome",
            "License Agreement", 
            "Installation Directory",
            "Installation Options",
            "Installing",
            "Completion"
        ]
        
        self.create_interface()
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
    
    def create_interface(self):
        """Create setup interface"""
        # Header frame
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Logo and title
        title_label = tk.Label(
            header_frame,
            text=self.app_name,
            bg="#2c3e50",
            fg="white",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text=f"Setup Wizard - Version {self.app_version}",
            bg="#2c3e50",
            fg="#bdc3c7",
            font=("Arial", 10)
        )
        subtitle_label.pack()
        
        # Progress frame
        progress_frame = tk.Frame(self.root, bg="#ecf0f1", height=30)
        progress_frame.pack(fill="x")
        progress_frame.pack_propagate(False)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=len(self.steps) - 1,
            length=580
        )
        self.progress_bar.pack(pady=5)
        
        # Main content frame
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0", height=50)
        button_frame.pack(fill="x", side="bottom")
        button_frame.pack_propagate(False)
        
        # Buttons
        self.back_btn = tk.Button(
            button_frame,
            text="< Back",
            command=self.go_back,
            state="disabled",
            width=10
        )
        self.back_btn.pack(side="left", padx=10, pady=10)
        
        self.next_btn = tk.Button(
            button_frame,
            text="Next >",
            command=self.go_next,
            width=10,
            bg="#3498db",
            fg="white",
            font=("Arial", 9, "bold")
        )
        self.next_btn.pack(side="right", padx=10, pady=10)
        
        self.cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_setup,
            width=10
        )
        self.cancel_btn.pack(side="right", padx=(0, 10), pady=10)
        
        # Show first step
        self.show_step()
    
    def show_step(self):
        """Show current setup step"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Update progress
        self.progress_var.set(self.current_step)
        
        # Show appropriate step
        if self.current_step == 0:
            self.show_welcome()
        elif self.current_step == 1:
            self.show_license()
        elif self.current_step == 2:
            self.show_directory()
        elif self.current_step == 3:
            self.show_options()
        elif self.current_step == 4:
            self.show_installation()
        elif self.current_step == 5:
            self.show_completion()
        
        # Update buttons
        self.update_buttons()
    
    def show_welcome(self):
        """Show welcome step"""
        welcome_frame = tk.Frame(self.content_frame, bg="white")
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome title
        title_label = tk.Label(
            welcome_frame,
            text=f"Welcome to {self.app_name} Setup",
            bg="white",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Welcome message
        message = f"""This wizard will guide you through the installation of {self.app_name}.

{self.app_name} is a comprehensive hospital management solution designed for healthcare facilities to manage patients, appointments, billing, lab tests, and generate detailed reports.

Publisher: {self.publisher}
Version: {self.app_version}
Release Date: {datetime.now().strftime('%B %Y')}

Key Features:
• Patient Management with Medical History
• Advanced Appointment Scheduling
• Comprehensive Billing System
• Lab Test Management with Results
• Reports & Analytics with Charts
• User Management with Role-based Access
• Modern Dark Theme Interface

Click Next to continue with the installation."""
        
        message_label = tk.Label(
            welcome_frame,
            text=message,
            bg="white",
            font=("Arial", 10),
            justify="left",
            wraplength=500
        )
        message_label.pack(pady=10)
        
        # System requirements
        req_frame = tk.LabelFrame(welcome_frame, text="System Requirements", bg="white", font=("Arial", 9, "bold"))
        req_frame.pack(fill="x", pady=20)
        
        requirements = """• Windows 10 or higher
• Python 3.7 or higher
• 4GB RAM minimum (8GB recommended)
• 100MB free disk space
• 1366x768 minimum screen resolution"""
        
        req_label = tk.Label(
            req_frame,
            text=requirements,
            bg="white",
            font=("Arial", 9),
            justify="left"
        )
        req_label.pack(padx=10, pady=10)
    
    def show_license(self):
        """Show license agreement step"""
        license_frame = tk.Frame(self.content_frame, bg="white")
        license_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # License title
        title_label = tk.Label(
            license_frame,
            text="End User License Agreement",
            bg="white",
            font=("Arial", 14, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 10))
        
        # License text
        license_text = scrolledtext.ScrolledText(
            license_frame,
            height=15,
            width=70,
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        license_text.pack(fill="both", expand=True, pady=(0, 10))
        
        # Insert license agreement
        eula_text = self.get_license_text()
        license_text.insert("1.0", eula_text)
        license_text.config(state="disabled")
        
        # Agreement checkbox
        agreement_frame = tk.Frame(license_frame, bg="white")
        agreement_frame.pack(fill="x")
        
        self.agreement_var = tk.BooleanVar()
        agreement_check = tk.Checkbutton(
            agreement_frame,
            text="I accept the terms in the License Agreement",
            variable=self.agreement_var,
            bg="white",
            font=("Arial", 10, "bold"),
            command=self.on_agreement_change
        )
        agreement_check.pack(anchor="w")
    
    def show_directory(self):
        """Show installation directory step"""
        dir_frame = tk.Frame(self.content_frame, bg="white")
        dir_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Directory title
        title_label = tk.Label(
            dir_frame,
            text="Choose Installation Location",
            bg="white",
            font=("Arial", 14, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Directory message
        message_label = tk.Label(
            dir_frame,
            text="Setup will install the application in the following folder.\nTo install in a different folder, click Browse and select another folder.",
            bg="white",
            font=("Arial", 10),
            justify="left"
        )
        message_label.pack(pady=(0, 20))
        
        # Directory selection
        dir_selection_frame = tk.Frame(dir_frame, bg="white")
        dir_selection_frame.pack(fill="x", pady=10)
        
        dir_label = tk.Label(
            dir_selection_frame,
            text="Destination Folder:",
            bg="white",
            font=("Arial", 10, "bold")
        )
        dir_label.pack(anchor="w")
        
        dir_entry_frame = tk.Frame(dir_selection_frame, bg="white")
        dir_entry_frame.pack(fill="x", pady=5)
        
        # Default installation directory
        default_dir = os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), self.publisher, self.app_name)
        self.install_dir_var = tk.StringVar(value=default_dir)
        
        dir_entry = tk.Entry(
            dir_entry_frame,
            textvariable=self.install_dir_var,
            font=("Arial", 10),
            width=50
        )
        dir_entry.pack(side="left", fill="x", expand=True)
        
        browse_btn = tk.Button(
            dir_entry_frame,
            text="Browse...",
            command=self.browse_directory,
            width=10
        )
        browse_btn.pack(side="right", padx=(5, 0))
        
        # Space requirements
        space_frame = tk.LabelFrame(dir_frame, text="Disk Space Requirements", bg="white", font=("Arial", 9, "bold"))
        space_frame.pack(fill="x", pady=20)
        
        space_info = """Space required: 100 MB
Space available: Calculating..."""
        
        self.space_label = tk.Label(
            space_frame,
            text=space_info,
            bg="white",
            font=("Arial", 9),
            justify="left"
        )
        self.space_label.pack(padx=10, pady=10)
        
        # Calculate available space
        self.calculate_space()
    
    def show_options(self):
        """Show installation options step"""
        options_frame = tk.Frame(self.content_frame, bg="white")
        options_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Options title
        title_label = tk.Label(
            options_frame,
            text="Installation Options",
            bg="white",
            font=("Arial", 14, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Shortcuts options
        shortcuts_frame = tk.LabelFrame(options_frame, text="Shortcuts", bg="white", font=("Arial", 10, "bold"))
        shortcuts_frame.pack(fill="x", pady=10)
        
        self.desktop_shortcut_var = tk.BooleanVar(value=True)
        desktop_check = tk.Checkbutton(
            shortcuts_frame,
            text="Create desktop shortcut",
            variable=self.desktop_shortcut_var,
            bg="white",
            font=("Arial", 10)
        )
        desktop_check.pack(anchor="w", padx=10, pady=5)
        
        self.startmenu_shortcut_var = tk.BooleanVar(value=True)
        startmenu_check = tk.Checkbutton(
            shortcuts_frame,
            text="Create Start Menu shortcut",
            variable=self.startmenu_shortcut_var,
            bg="white",
            font=("Arial", 10)
        )
        startmenu_check.pack(anchor="w", padx=10, pady=5)
        
        # Additional options
        additional_frame = tk.LabelFrame(options_frame, text="Additional Options", bg="white", font=("Arial", 10, "bold"))
        additional_frame.pack(fill="x", pady=10)
        
        self.auto_start_var = tk.BooleanVar(value=False)
        auto_start_check = tk.Checkbutton(
            additional_frame,
            text="Launch application after installation",
            variable=self.auto_start_var,
            bg="white",
            font=("Arial", 10)
        )
        auto_start_check.pack(anchor="w", padx=10, pady=5)
        
        self.register_var = tk.BooleanVar(value=True)
        register_check = tk.Checkbutton(
            additional_frame,
            text="Register application in Windows Programs",
            variable=self.register_var,
            bg="white",
            font=("Arial", 10)
        )
        register_check.pack(anchor="w", padx=10, pady=5)
        
        # Installation summary
        summary_frame = tk.LabelFrame(options_frame, text="Installation Summary", bg="white", font=("Arial", 10, "bold"))
        summary_frame.pack(fill="x", pady=20)
        
        summary_text = f"""Application: {self.app_name}
Version: {self.app_version}
Publisher: {self.publisher}
Installation Directory: {self.install_dir_var.get()}
Required Space: 100 MB"""
        
        summary_label = tk.Label(
            summary_frame,
            text=summary_text,
            bg="white",
            font=("Arial", 9),
            justify="left"
        )
        summary_label.pack(padx=10, pady=10)
    
    def show_installation(self):
        """Show installation progress step"""
        install_frame = tk.Frame(self.content_frame, bg="white")
        install_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Installation title
        title_label = tk.Label(
            install_frame,
            text="Installing Hospital Management System",
            bg="white",
            font=("Arial", 14, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Status label
        self.status_label = tk.Label(
            install_frame,
            text="Preparing installation...",
            bg="white",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=10)
        
        # Installation progress
        self.install_progress_var = tk.DoubleVar()
        install_progress = ttk.Progressbar(
            install_frame,
            variable=self.install_progress_var,
            maximum=100,
            length=500,
            mode='determinate'
        )
        install_progress.pack(pady=20)
        
        # Installation log
        log_frame = tk.LabelFrame(install_frame, text="Installation Log", bg="white", font=("Arial", 9, "bold"))
        log_frame.pack(fill="both", expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            width=70,
            font=("Consolas", 8),
            wrap=tk.WORD
        )
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Start installation
        self.root.after(1000, self.start_installation)
    
    def show_completion(self):
        """Show installation completion step"""
        complete_frame = tk.Frame(self.content_frame, bg="white")
        complete_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Completion title
        title_label = tk.Label(
            complete_frame,
            text="Installation Complete",
            bg="white",
            font=("Arial", 16, "bold"),
            fg="#27ae60"
        )
        title_label.pack(pady=(0, 20))
        
        # Success message
        message = f"""{self.app_name} has been successfully installed on your computer.

The application is now ready to use with the following features:
• Patient Management System
• Appointment Scheduling
• Billing and Payment Tracking
• Lab Test Management
• Reports and Analytics
• User Management

Default Login Credentials:
Username: admin
Password: admin123

Thank you for choosing {self.publisher} solutions!"""
        
        message_label = tk.Label(
            complete_frame,
            text=message,
            bg="white",
            font=("Arial", 10),
            justify="left",
            wraplength=500
        )
        message_label.pack(pady=10)
        
        # Launch option
        if self.auto_start_var.get():
            launch_frame = tk.Frame(complete_frame, bg="white")
            launch_frame.pack(fill="x", pady=20)
            
            launch_label = tk.Label(
                launch_frame,
                text="✓ Application will launch automatically when you click Finish",
                bg="white",
                font=("Arial", 10, "bold"),
                fg="#27ae60"
            )
            launch_label.pack()
    
    def get_license_text(self):
        """Get the End User License Agreement text"""
        return f"""END USER LICENSE AGREEMENT

{self.app_name}
Version {self.app_version}
Publisher: {self.publisher}

IMPORTANT - READ CAREFULLY: This End User License Agreement ("EULA") is a legal agreement between you (either an individual or a single entity) and {self.publisher} for the software product identified above, which includes computer software and may include associated media, printed materials, and "online" or electronic documentation ("SOFTWARE PRODUCT").

By installing, copying, or otherwise using the SOFTWARE PRODUCT, you agree to be bound by the terms of this EULA. If you do not agree to the terms of this EULA, do not install or use the SOFTWARE PRODUCT.

1. GRANT OF LICENSE
{self.publisher} grants you the following rights provided that you comply with all terms and conditions of this EULA:

a) Installation and Use: You may install and use one copy of the SOFTWARE PRODUCT on a single computer.
b) Backup Copy: You may make one backup copy of the SOFTWARE PRODUCT for archival purposes only.

2. DESCRIPTION OF OTHER RIGHTS AND LIMITATIONS

a) Limitations on Reverse Engineering, Decompilation, and Disassembly: You may not reverse engineer, decompile, or disassemble the SOFTWARE PRODUCT.

b) No Rental/Commercial Hosting: You may not rent, lease, lend, or provide commercial hosting services with the SOFTWARE PRODUCT.

c) Software Transfer: You may permanently transfer all of your rights under this EULA, provided the recipient agrees to the terms of this EULA.

3. TERMINATION
Without prejudice to any other rights, {self.publisher} may terminate this EULA if you fail to comply with the terms and conditions of this EULA.

4. COPYRIGHT
All title and copyrights in and to the SOFTWARE PRODUCT (including but not limited to any images, photographs, animations, video, audio, music, text, and "applets" incorporated into the SOFTWARE PRODUCT), the accompanying printed materials, and any copies of the SOFTWARE PRODUCT are owned by {self.publisher}.

5. NO WARRANTIES
{self.publisher} expressly disclaims any warranty for the SOFTWARE PRODUCT. The SOFTWARE PRODUCT and any related documentation is provided "as is" without warranty of any kind, either express or implied.

6. LIMITATION OF LIABILITY
In no event shall {self.publisher} be liable for any damages whatsoever (including, without limitation, damages for loss of business profits, business interruption, loss of business information, or any other pecuniary loss) arising out of the use of or inability to use this product.

7. HEALTHCARE COMPLIANCE
This software is designed for healthcare management purposes. Users are responsible for ensuring compliance with applicable healthcare regulations including but not limited to HIPAA, local privacy laws, and medical record keeping requirements.

8. DATA SECURITY
Users are responsible for implementing appropriate security measures to protect patient data and sensitive information. {self.publisher} recommends regular backups and security updates.

9. SUPPORT AND UPDATES
{self.publisher} may provide updates and support for the SOFTWARE PRODUCT at its discretion. Updates may be provided free of charge or may require additional licensing fees.

10. GOVERNING LAW
This EULA shall be governed by the laws of the jurisdiction where {self.publisher} is located.

By clicking "I accept the terms in the License Agreement" below, you acknowledge that you have read this agreement, understand it, and agree to be bound by its terms and conditions.

Copyright © {datetime.now().year} {self.publisher}. All rights reserved.

Contact Information:
{self.publisher}
Email: support@kaitsnet.com
Website: www.kaitsnet.com

Last Updated: {datetime.now().strftime('%B %d, %Y')}"""
    
    def browse_directory(self):
        """Browse for installation directory"""
        from tkinter import filedialog
        directory = filedialog.askdirectory(
            title="Select Installation Directory",
            initialdir=self.install_dir_var.get()
        )
        if directory:
            self.install_dir_var.set(directory)
            self.calculate_space()
    
    def calculate_space(self):
        """Calculate available disk space"""
        try:
            import shutil
            directory = os.path.dirname(self.install_dir_var.get())
            if not os.path.exists(directory):
                directory = "C:\\"
            
            total, used, free = shutil.disk_usage(directory)
            free_mb = free // (1024 * 1024)
            
            space_info = f"""Space required: 100 MB
Space available: {free_mb:,} MB"""
            
            if hasattr(self, 'space_label'):
                self.space_label.config(text=space_info)
                
        except Exception:
            if hasattr(self, 'space_label'):
                self.space_label.config(text="Space required: 100 MB\nSpace available: Unable to calculate")
    
    def on_agreement_change(self):
        """Handle license agreement checkbox change"""
        self.agreement_accepted = self.agreement_var.get()
        self.update_buttons()
    
    def update_buttons(self):
        """Update button states"""
        # Back button
        if self.current_step == 0:
            self.back_btn.config(state="disabled")
        else:
            self.back_btn.config(state="normal")
        
        # Next button
        if self.current_step == len(self.steps) - 1:
            self.next_btn.config(text="Finish", bg="#27ae60")
        elif self.current_step == len(self.steps) - 2:  # Installation step
            self.next_btn.config(state="disabled")
        elif self.current_step == 1 and not self.agreement_accepted:  # License step
            self.next_btn.config(state="disabled")
        else:
            self.next_btn.config(state="normal", text="Next >", bg="#3498db")
        
        # Cancel button
        if self.current_step == len(self.steps) - 1:
            self.cancel_btn.config(state="disabled")
    
    def go_back(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step()
    
    def go_next(self):
        """Go to next step"""
        if self.current_step < len(self.steps) - 1:
            if self.current_step == 2:  # Directory step
                self.install_dir = self.install_dir_var.get()
            
            self.current_step += 1
            self.show_step()
        else:
            # Finish installation
            self.finish_installation()
    
    def cancel_setup(self):
        """Cancel setup"""
        result = messagebox.askyesno(
            "Cancel Setup",
            "Are you sure you want to cancel the installation?"
        )
        if result:
            self.root.destroy()
    
    def start_installation(self):
        """Start the installation process"""
        self.install_progress_var.set(0)
        self.log_message("Starting installation...")
        
        try:
            # Step 1: Create directories
            self.log_message("Creating installation directories...")
            self.install_progress_var.set(10)
            self.root.update()
            
            os.makedirs(self.install_dir, exist_ok=True)
            self.log_message(f"Created directory: {self.install_dir}")
            
            # Step 2: Copy application files
            self.log_message("Copying application files...")
            self.install_progress_var.set(30)
            self.root.update()
            
            source_dir = os.path.dirname(os.path.abspath(__file__))
            self.copy_application_files(source_dir, self.install_dir)
            
            # Step 3: Install Python dependencies
            self.log_message("Installing Python dependencies...")
            self.install_progress_var.set(50)
            self.root.update()
            
            self.install_dependencies()
            
            # Step 4: Create shortcuts
            if self.desktop_shortcut_var.get() or self.startmenu_shortcut_var.get():
                self.log_message("Creating shortcuts...")
                self.install_progress_var.set(70)
                self.root.update()
                
                self.create_shortcuts()
            
            # Step 5: Register application
            if self.register_var.get():
                self.log_message("Registering application...")
                self.install_progress_var.set(85)
                self.root.update()
                
                self.register_application()
            
            # Step 6: Create uninstaller
            self.log_message("Creating uninstaller...")
            self.install_progress_var.set(95)
            self.root.update()
            
            self.create_uninstaller()
            
            # Complete
            self.log_message("Installation completed successfully!")
            self.install_progress_var.set(100)
            self.root.update()
            
            # Enable next button
            self.next_btn.config(state="normal")
            
        except Exception as e:
            self.log_message(f"Installation failed: {str(e)}")
            messagebox.showerror("Installation Error", f"Installation failed: {str(e)}")
    
    def copy_application_files(self, source_dir, dest_dir):
        """Copy application files to installation directory"""
        files_to_copy = [
            "desktop_app.py",
            "patient_management.py",
            "appointment_management.py",
            "billing_management.py",
            "lab_management.py",
            "reports_management.py",
            "user_management.py",
            "launch.py",
            "requirements.txt",
            "README.md"
        ]
        
        for file_name in files_to_copy:
            source_file = os.path.join(source_dir, file_name)
            if os.path.exists(source_file):
                dest_file = os.path.join(dest_dir, file_name)
                shutil.copy2(source_file, dest_file)
                self.log_message(f"Copied: {file_name}")
    
    def install_dependencies(self):
        """Install Python dependencies"""
        try:
            packages = [
                "tkcalendar==1.6.1",
                "matplotlib==3.7.2", 
                "pandas==2.0.3",
                "Pillow==10.0.0"
            ]
            
            for package in packages:
                self.log_message(f"Installing {package}...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", package],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    self.log_message(f"✓ {package} installed successfully")
                else:
                    self.log_message(f"✗ Failed to install {package}")
                    
        except Exception as e:
            self.log_message(f"Error installing dependencies: {str(e)}")
    
    def create_shortcuts(self):
        """Create desktop and start menu shortcuts"""
        try:
            if self.desktop_shortcut_var.get():
                self.create_desktop_shortcut()
            
            if self.startmenu_shortcut_var.get():
                self.create_startmenu_shortcut()
                
        except Exception as e:
            self.log_message(f"Error creating shortcuts: {str(e)}")
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut"""
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, f"{self.app_name}.lnk")
            target = os.path.join(self.install_dir, "launch.py")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = self.install_dir
            shortcut.Description = f"{self.app_name} - {self.publisher}"
            shortcut.save()
            
            self.log_message("✓ Desktop shortcut created")
            
        except ImportError:
            self.log_message("! Desktop shortcut creation skipped (winshell not available)")
        except Exception as e:
            self.log_message(f"! Desktop shortcut creation failed: {str(e)}")
    
    def create_startmenu_shortcut(self):
        """Create start menu shortcut"""
        try:
            import winshell
            from win32com.client import Dispatch
            
            start_menu = winshell.start_menu()
            app_folder = os.path.join(start_menu, self.publisher)
            os.makedirs(app_folder, exist_ok=True)
            
            shortcut_path = os.path.join(app_folder, f"{self.app_name}.lnk")
            target = os.path.join(self.install_dir, "launch.py")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = self.install_dir
            shortcut.Description = f"{self.app_name} - {self.publisher}"
            shortcut.save()
            
            self.log_message("✓ Start Menu shortcut created")
            
        except ImportError:
            self.log_message("! Start Menu shortcut creation skipped (winshell not available)")
        except Exception as e:
            self.log_message(f"! Start Menu shortcut creation failed: {str(e)}")
    
    def register_application(self):
        """Register application in Windows registry"""
        try:
            # Register in Programs and Features
            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            app_reg_path = f"{reg_path}\\{self.app_id}"
            
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, app_reg_path) as key:
                winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, self.app_name)
                winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, self.app_version)
                winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, self.publisher)
                winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, self.install_dir)
                winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, 
                                os.path.join(self.install_dir, "uninstall.exe"))
                winreg.SetValueEx(key, "EstimatedSize", 0, winreg.REG_DWORD, 102400)  # 100MB in KB
                winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "InstallDate", 0, winreg.REG_SZ, 
                                datetime.now().strftime("%Y%m%d"))
            
            self.log_message("✓ Application registered in Windows")
            
        except Exception as e:
            self.log_message(f"! Application registration failed: {str(e)}")
    
    def create_uninstaller(self):
        """Create uninstaller script"""
        uninstaller_content = f'''"""
{self.app_name} Uninstaller
Publisher: {self.publisher}
"""

import os
import sys
import shutil
import winreg
from tkinter import messagebox

def uninstall():
    """Uninstall the application"""
    try:
        # Remove registry entries
        try:
            reg_path = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{self.app_id}"
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
        except:
            pass
        
        # Remove shortcuts
        try:
            import winshell
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "{self.app_name}.lnk")
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
        except:
            pass
        
        # Remove start menu shortcuts
        try:
            import winshell
            start_menu = winshell.start_menu()
            app_folder = os.path.join(start_menu, "{self.publisher}")
            if os.path.exists(app_folder):
                shutil.rmtree(app_folder)
        except:
            pass
        
        messagebox.showinfo("Uninstall Complete", "{self.app_name} has been successfully removed from your computer.")
        
        # Remove installation directory (except uninstaller)
        install_dir = os.path.dirname(os.path.abspath(__file__))
        for item in os.listdir(install_dir):
            if item != "uninstall.exe":
                item_path = os.path.join(install_dir, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
        
    except Exception as e:
        messagebox.showerror("Uninstall Error", f"Error during uninstallation: {{str(e)}}")

if __name__ == "__main__":
    result = messagebox.askyesno(
        "Uninstall {self.app_name}",
        "Are you sure you want to remove {self.app_name} from your computer?"
    )
    if result:
        uninstall()
'''
        
        uninstaller_path = os.path.join(self.install_dir, "uninstall.py")
        with open(uninstaller_path, 'w') as f:
            f.write(uninstaller_content)
        
        self.log_message("✓ Uninstaller created")
    
    def log_message(self, message):
        """Add message to installation log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update()
    
    def finish_installation(self):
        """Finish installation and close setup"""
        if self.auto_start_var.get():
            try:
                launch_script = os.path.join(self.install_dir, "launch.py")
                subprocess.Popen([sys.executable, launch_script])
            except Exception as e:
                messagebox.showerror("Launch Error", f"Could not launch application: {str(e)}")
        
        self.root.destroy()
    
    def run(self):
        """Run the setup installer"""
        self.root.mainloop()

def main():
    """Main setup function"""
    # Check if running as administrator (recommended for installation)
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            messagebox.showwarning(
                "Administrator Rights",
                "For best results, run this installer as Administrator.\n\n"
                "Right-click the installer and select 'Run as administrator'."
            )
    except:
        pass
    
    # Create and run installer
    installer = SetupInstaller()
    installer.run()

if __name__ == "__main__":
    main()