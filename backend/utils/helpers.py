"""
Helper utilities for GearGuard Admin Panel
"""

from datetime import datetime
from functools import wraps
from flask import jsonify

def format_date(date_string, format='%Y-%m-%d'):
    """Format date string"""
    try:
        date_obj = datetime.strptime(date_string, format)
        return date_obj.strftime('%b %d, %Y')
    except:
        return date_string

def calculate_days_between(start_date, end_date):
    """Calculate days between two dates"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        delta = end - start
        return delta.days
    except:
        return 0

def validate_required_fields(data, required_fields):
    """Validate that required fields are present in data"""
    missing = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            missing.append(field)
    return missing

def error_response(message, status_code=400):
    """Create error response"""
    return jsonify({
        'success': False,
        'error': message
    }), status_code

def success_response(data=None, message=None, status_code=200):
    """Create success response"""
    response = {'success': True}
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    return jsonify(response), status_code

def handle_errors(f):
    """Decorator to handle errors in routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return error_response(str(e), 400)
        except KeyError as e:
            return error_response(f"Missing key: {str(e)}", 400)
        except Exception as e:
            return error_response(f"Internal server error: {str(e)}", 500)
    return decorated_function

def get_status_badge_class(status):
    """Get CSS class for status badge"""
    status_classes = {
        'operational': 'badge-success',
        'maintenance': 'badge-warning',
        'breakdown': 'badge-danger',
        'scrap': 'badge-secondary',
        'new': 'badge-info',
        'in_progress': 'badge-warning',
        'repaired': 'badge-success',
        'scheduled': 'badge-info',
        'overdue': 'badge-danger',
        'completed': 'badge-success',
        'active': 'badge-success',
        'inactive': 'badge-secondary'
    }
    return status_classes.get(status, 'badge-secondary')

def get_priority_badge_class(priority):
    """Get CSS class for priority badge"""
    priority_classes = {
        'low': 'badge-info',
        'medium': 'badge-warning',
        'high': 'badge-danger',
        'critical': 'badge-danger-dark'
    }
    return priority_classes.get(priority, 'badge-secondary')
