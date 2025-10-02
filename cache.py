"""
Caching module for MediManage
Provides caching functionality to improve performance
"""

import time
import json
import functools
import hashlib
from datetime import datetime, timedelta
from flask import current_app, g

# Simple in-memory cache
_cache = {}

def cache_key(*args, **kwargs):
    """Generate a cache key from function arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
    key = hashlib.md5(":".join(key_parts).encode()).hexdigest()
    return key

def cache(ttl=300):
    """Cache decorator with time-to-live in seconds"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Skip cache in debug mode if configured
            if current_app.config.get('DEBUG') and current_app.config.get('DISABLE_CACHE_IN_DEBUG', False):
                return func(*args, **kwargs)
            
            # Generate cache key
            key = f"{func.__module__}.{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Check if result is in cache and not expired
            if key in _cache:
                result, timestamp = _cache[key]
                if time.time() - timestamp < ttl:
                    return result
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            _cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator

def role_based_cache(ttl=300):
    """Cache decorator that includes user role in the cache key"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Skip cache in debug mode if configured
            if current_app.config.get('DEBUG') and current_app.config.get('DISABLE_CACHE_IN_DEBUG', False):
                return func(*args, **kwargs)
            
            # Include user role in cache key if available
            role = g.user.role if hasattr(g, 'user') and g.user else 'anonymous'
            
            # Generate cache key
            key = f"{func.__module__}.{func.__name__}:{role}:{cache_key(*args, **kwargs)}"
            
            # Check if result is in cache and not expired
            if key in _cache:
                result, timestamp = _cache[key]
                if time.time() - timestamp < ttl:
                    return result
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            _cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator

def user_based_cache(ttl=300):
    """Cache decorator that includes user ID in the cache key"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Skip cache in debug mode if configured
            if current_app.config.get('DEBUG') and current_app.config.get('DISABLE_CACHE_IN_DEBUG', False):
                return func(*args, **kwargs)
            
            # Include user ID in cache key if available
            user_id = g.user.id if hasattr(g, 'user') and g.user else 'anonymous'
            
            # Generate cache key
            key = f"{func.__module__}.{func.__name__}:{user_id}:{cache_key(*args, **kwargs)}"
            
            # Check if result is in cache and not expired
            if key in _cache:
                result, timestamp = _cache[key]
                if time.time() - timestamp < ttl:
                    return result
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            _cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator

def invalidate_cache(pattern=None):
    """Invalidate cache entries matching the pattern"""
    global _cache
    if pattern is None:
        _cache = {}
    else:
        _cache = {k: v for k, v in _cache.items() if pattern not in k}

def get_cache_stats():
    """Get cache statistics"""
    return {
        'size': len(_cache),
        'keys': list(_cache.keys()),
        'memory_usage': sum(len(str(v[0])) for v in _cache.values())
    }

# Model-specific cache invalidation functions
def invalidate_patient_cache(patient_id=None):
    """Invalidate patient-related cache entries"""
    if patient_id:
        invalidate_cache(f"patient:{patient_id}")
    else:
        invalidate_cache("patient")
        invalidate_cache("dashboard")
        invalidate_cache("analytics")

def invalidate_appointment_cache(appointment_id=None):
    """Invalidate appointment-related cache entries"""
    if appointment_id:
        invalidate_cache(f"appointment:{appointment_id}")
    else:
        invalidate_cache("appointment")
        invalidate_cache("dashboard")
        invalidate_cache("analytics")

def invalidate_bill_cache(bill_id=None):
    """Invalidate billing-related cache entries"""
    if bill_id:
        invalidate_cache(f"bill:{bill_id}")
    else:
        invalidate_cache("bill")
        invalidate_cache("dashboard")
        invalidate_cache("analytics")

def invalidate_lab_cache(test_id=None):
    """Invalidate lab test-related cache entries"""
    if test_id:
        invalidate_cache(f"lab:{test_id}")
    else:
        invalidate_cache("lab")
        invalidate_cache("dashboard")
        invalidate_cache("analytics")

def invalidate_user_cache(user_id=None):
    """Invalidate user-related cache entries"""
    if user_id:
        invalidate_cache(f"user:{user_id}")
    else:
        invalidate_cache("user")

# Database query optimization functions
class QueryOptimizer:
    """Helper class for optimizing database queries"""
    
    @staticmethod
    def paginate_query(query, page, per_page=20):
        """Paginate a query to improve performance"""
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def optimize_patient_query(query, include_relationships=False):
        """Optimize a patient query"""
        if include_relationships:
            return query.options(
                db.joinedload(Patient.appointments),
                db.joinedload(Patient.bills),
                db.joinedload(Patient.lab_tests)
            )
        return query
    
    @staticmethod
    def optimize_appointment_query(query, include_relationships=False):
        """Optimize an appointment query"""
        if include_relationships:
            return query.options(
                db.joinedload(Appointment.patient),
                db.joinedload(Appointment.doctor)
            )
        return query
    
    @staticmethod
    def optimize_bill_query(query, include_relationships=False):
        """Optimize a bill query"""
        if include_relationships:
            return query.options(
                db.joinedload(Bill.patient),
                db.joinedload(Bill.items)
            )
        return query
    
    @staticmethod
    def optimize_lab_query(query, include_relationships=False):
        """Optimize a lab test query"""
        if include_relationships:
            return query.options(
                db.joinedload(LabTest.patient),
                db.joinedload(LabTest.ordered_by_user)
            )
        return query