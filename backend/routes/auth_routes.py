"""
Authentication Routes
API endpoints for user authentication (login, signup, logout)
"""

from flask import Blueprint, request, jsonify, session
import hashlib
import secrets
from datetime import datetime
from backend.database.db import db

auth_bp = Blueprint('auth', __name__)

# In-memory token store (in production, use Redis or database)
active_tokens = {}

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    """Create new user account"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        
        # Validate required fields
        if not email or not password or not full_name:
            return jsonify({
                'success': False,
                'error': 'All fields are required'
            }), 400
        
        # Validate email is Gmail
        if not email.endswith('@gmail.com'):
            return jsonify({
                'success': False,
                'error': 'Only Gmail addresses are allowed'
            }), 400
        
        # Validate password length
        if len(password) < 8:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 8 characters'
            }), 400
        
        # Check if user already exists
        check_query = "SELECT id FROM users WHERE email = %s"
        existing_user = db.execute_query(check_query, (email,), fetch_one=True)
        
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 400
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Create user
        insert_query = """
            INSERT INTO users (email, password, full_name, created_at)
            VALUES (%s, %s, %s, NOW())
        """
        user_id = db.execute_query(
            insert_query, 
            (email, hashed_password, full_name), 
            fetch_all=False
        )
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'user': {
                'id': user_id,
                'email': email,
                'full_name': full_name
            }
        }), 201
        
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Unable to create account. Please try again.'
        }), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Authenticate user and create session"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validate required fields
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Hash password for comparison
        hashed_password = hash_password(password)
        
        # Find user
        query = """
            SELECT id, email, full_name, created_at 
            FROM users 
            WHERE email = %s AND password = %s
        """
        user = db.execute_query(query, (email, hashed_password), fetch_one=True)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
        
        # Update last login
        update_query = "UPDATE users SET last_login = NOW() WHERE id = %s"
        db.execute_query(update_query, (user['id'],), fetch_all=False)
        
        # Generate token
        token = generate_token()
        active_tokens[token] = {
            'user_id': user['id'],
            'email': user['email'],
            'full_name': user.get('full_name'),
            'created_at': datetime.now().isoformat()
        }
        
        # Set session
        session['user_id'] = user['id']
        session['email'] = user['email']
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'full_name': user.get('full_name')
            }
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Login failed. Please try again.'
        }), 500

@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    """Logout user and invalidate token"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            if token in active_tokens:
                del active_tokens[token]
        
        # Clear session
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        print(f"Logout error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Logout failed'
        }), 500

@auth_bp.route('/auth/verify', methods=['GET'])
def verify_token():
    """Verify if token is valid"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'No token provided'
            }), 401
        
        token = auth_header[7:]
        
        if token in active_tokens:
            user_data = active_tokens[token]
            return jsonify({
                'success': True,
                'user': {
                    'email': user_data['email'],
                    'full_name': user_data.get('full_name')
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401
            
    except Exception as e:
        print(f"Verify token error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Token verification failed'
        }), 500

@auth_bp.route('/auth/me', methods=['GET'])
def get_current_user():
    """Get current logged in user"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Not authenticated'
            }), 401
        
        token = auth_header[7:]
        
        if token not in active_tokens:
            return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
        
        user_data = active_tokens[token]
        
        return jsonify({
            'success': True,
            'user': {
                'email': user_data['email'],
                'full_name': user_data.get('full_name')
            }
        }), 200
        
    except Exception as e:
        print(f"Get current user error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get user'
        }), 500
