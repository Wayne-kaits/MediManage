from datetime import datetime, date
from flask import request

class FormValidator:
    def __init__(self, data):
        self.data = data
        self.errors = {}

    def required(self, field, message=None):
        if not self.data.get(field) or str(self.data.get(field)).strip() == '':
            self.errors[field] = message or f'{field} is required'
        return self

    def email(self, field, message=None):
        value = self.data.get(field)
        if value and '@' not in value:
            self.errors[field] = message or 'Invalid email format'
        return self

    def min_length(self, field, length, message=None):
        value = self.data.get(field)
        if value and len(str(value)) < length:
            self.errors[field] = message or f'{field} must be at least {length} characters'
        return self

    def date_format(self, field, message=None):
        value = self.data.get(field)
        if value:
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                self.errors[field] = message or 'Invalid date format (YYYY-MM-DD)'
        return self

    def datetime_format(self, field, message=None):
        value = self.data.get(field)
        if value:
            try:
                datetime.strptime(value, '%Y-%m-%dT%H:%M')
            except ValueError:
                self.errors[field] = message or 'Invalid datetime format'
        return self

    def numeric(self, field, message=None):
        value = self.data.get(field)
        if value:
            try:
                float(value)
            except ValueError:
                self.errors[field] = message or f'{field} must be a number'
        return self

    def is_valid(self):
        return len(self.errors) == 0

def validate_user_form(data):
    validator = FormValidator(data)
    return (validator
            .required('username')
            .required('email')
            .required('password')
            .required('first_name')
            .required('last_name')
            .required('role')
            .email('email')
            .min_length('password', 6))

def validate_patient_form(data):
    validator = FormValidator(data)
    return (validator
            .required('first_name')
            .required('last_name')
            .required('date_of_birth')
            .required('gender')
            .date_format('date_of_birth')
            .email('email', 'Invalid email format (optional)'))

def validate_appointment_form(data):
    validator = FormValidator(data)
    return (validator
            .required('patient_id')
            .required('doctor_id')
            .required('appointment_date')
            .required('appointment_type')
            .datetime_format('appointment_date'))

def validate_bill_form(data):
    validator = FormValidator(data)
    return (validator
            .required('patient_id')
            .required('total_amount')
            .required('due_date')
            .numeric('total_amount')
            .date_format('due_date'))

def validate_lab_test_form(data):
    validator = FormValidator(data)
    return (validator
            .required('patient_id')
            .required('test_name')
            .required('test_type')
            .required('ordered_by'))
