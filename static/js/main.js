// Hospital Management System - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                if (bsAlert) {
                    bsAlert.close();
                }
            }, 5000);
        }
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
            form.classList.add('was-validated');
        });
    });

    // Search functionality enhancement
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="search"]');
    searchInputs.forEach(function(input) {
        let searchTimeout;
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                if (input.value.length >= 3 || input.value.length === 0) {
                    // Trigger search (in real implementation, this might be an AJAX call)
                    console.log('Searching for:', input.value);
                }
            }, 300);
        });
    });

    // Confirm dialogs for dangerous actions
    const dangerousActions = document.querySelectorAll('[data-confirm]');
    dangerousActions.forEach(function(element) {
        element.addEventListener('click', function(event) {
            const message = element.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                event.preventDefault();
                return false;
            }
        });
    });

    // Date input validation
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        // Set max date to today for birth dates
        if (input.name === 'date_of_birth') {
            const today = new Date();
            input.max = today.toISOString().split('T')[0];
        }
        
        // Set min date to today for future dates
        if (input.name === 'due_date' || input.name === 'appointment_date') {
            const today = new Date();
            input.min = today.toISOString().split('T')[0];
        }
    });

    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            let value = input.value.replace(/\D/g, '');
            if (value.length >= 6) {
                value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
            } else if (value.length >= 3) {
                value = value.replace(/(\d{3})(\d{3})/, '($1) $2');
            }
            input.value = value;
        });
    });

    // Currency formatting for amount inputs
    const currencyInputs = document.querySelectorAll('input[step="0.01"]');
    currencyInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (input.value) {
                const value = parseFloat(input.value);
                if (!isNaN(value)) {
                    input.value = value.toFixed(2);
                }
            }
        });
    });

    // Table row selection
    const selectableRows = document.querySelectorAll('.table tbody tr[data-selectable]');
    selectableRows.forEach(function(row) {
        row.addEventListener('click', function() {
            // Remove selection from other rows
            selectableRows.forEach(function(r) {
                r.classList.remove('table-active');
            });
            // Add selection to clicked row
            row.classList.add('table-active');
        });
    });

    // Loading states for buttons
    function showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Loading...';
        button.disabled = true;
    }

    function hideButtonLoading(button) {
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    // Apply loading states to form submissions
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const form = button.closest('form');
            if (form && form.checkValidity()) {
                showButtonLoading(button);
                
                // Hide loading after 5 seconds as fallback
                setTimeout(function() {
                    hideButtonLoading(button);
                }, 5000);
            }
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        // Ctrl+/ or Cmd+/ for search focus
        if ((event.ctrlKey || event.metaKey) && event.key === '/') {
            event.preventDefault();
            const searchInput = document.querySelector('input[type="search"], input[name="search"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to clear modals
        if (event.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(function(modal) {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) {
                    bsModal.hide();
                }
            });
        }
    });

    // Dynamic table filtering
    function filterTable(searchTerm, tableId) {
        const table = document.getElementById(tableId);
        if (!table) return;
        
        const rows = table.querySelectorAll('tbody tr');
        const searchLower = searchTerm.toLowerCase();
        
        rows.forEach(function(row) {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchLower)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    // Age calculation helper
    function calculateAge(birthDate) {
        const today = new Date();
        const birth = new Date(birthDate);
        let age = today.getFullYear() - birth.getFullYear();
        const monthDiff = today.getMonth() - birth.getMonth();
        
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
            age--;
        }
        
        return age;
    }

    // Update age displays
    const birthDateInputs = document.querySelectorAll('input[name="date_of_birth"]');
    birthDateInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const ageDisplay = document.getElementById('age-display');
            if (ageDisplay && input.value) {
                const age = calculateAge(input.value);
                ageDisplay.textContent = age + ' years old';
            }
        });
    });

    // Print functionality
    const printButtons = document.querySelectorAll('.btn-print, [onclick*="print"]');
    printButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            window.print();
        });
    });

    // Notification system (placeholder for future implementation)
    function showNotification(message, type = 'info') {
        // Create toast element
        const toastContainer = document.querySelector('.toast-container') || createToastContainer();
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    }

    function createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
        return container;
    }

    // Export functions for global use
    window.HMS = {
        showNotification: showNotification,
        calculateAge: calculateAge,
        filterTable: filterTable,
        showButtonLoading: showButtonLoading,
        hideButtonLoading: hideButtonLoading
    };

    // Initialize any page-specific functionality
    initializePageSpecific();
});

// Page-specific initialization
function initializePageSpecific() {
    const currentPage = window.location.pathname;
    
    // Dashboard specific
    if (currentPage.includes('/dashboard')) {
        initializeDashboard();
    }
    
    // Patient form specific
    if (currentPage.includes('/patients/add') || currentPage.includes('/patients/edit')) {
        initializePatientForm();
    }
    
    // Billing specific
    if (currentPage.includes('/billing/add')) {
        initializeBillingForm();
    }
    
    // Appointment specific
    if (currentPage.includes('/appointments/add')) {
        initializeAppointmentForm();
    }
}

function initializeDashboard() {
    // Auto-refresh dashboard stats every 5 minutes
    setInterval(function() {
        // In a real implementation, this would fetch updated stats
        console.log('Dashboard stats refresh (placeholder)');
    }, 300000);
}

function initializePatientForm() {
    // Patient ID generation preview
    const firstNameInput = document.querySelector('input[name="first_name"]');
    const lastNameInput = document.querySelector('input[name="last_name"]');
    
    if (firstNameInput && lastNameInput) {
        function updatePatientPreview() {
            const firstName = firstNameInput.value;
            const lastName = lastNameInput.value;
            
            if (firstName && lastName) {
                const preview = document.getElementById('patient-id-preview');
                if (preview) {
                    const today = new Date();
                    const dateStr = today.toISOString().slice(0, 10).replace(/-/g, '');
                    preview.textContent = `Preview ID: P${dateStr}XXXX`;
                }
            }
        }
        
        firstNameInput.addEventListener('input', updatePatientPreview);
        lastNameInput.addEventListener('input', updatePatientPreview);
    }
}

function initializeBillingForm() {
    // This is already handled in the template's inline script
    // Additional billing-specific functionality can be added here
}

function initializeAppointmentForm() {
    // Time slot availability checker (placeholder)
    const appointmentDateInput = document.querySelector('input[name="appointment_date"]');
    const doctorSelect = document.querySelector('select[name="doctor_id"]');
    
    if (appointmentDateInput && doctorSelect) {
        function checkAvailability() {
            const date = appointmentDateInput.value;
            const doctorId = doctorSelect.value;
            
            if (date && doctorId) {
                // In a real implementation, this would check doctor availability
                console.log('Checking availability for doctor', doctorId, 'on', date);
            }
        }
        
        appointmentDateInput.addEventListener('change', checkAvailability);
        doctorSelect.addEventListener('change', checkAvailability);
    }
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

function formatTime(time) {
    return new Intl.DateTimeFormat('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    }).format(new Date(time));
}

// Error handling
window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
    // In production, this might send error reports to a logging service
});

// Service worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Service worker registration would go here for offline functionality
        console.log('Service worker support detected');
    });
}
