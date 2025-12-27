"""
GearGuard Admin Panel - Main Application
Flask backend for maintenance management system
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import secrets

# Ensure project root is on sys.path so `import backend.*` works when running this file directly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.config import config
from backend.database.db import db

# Import blueprints
from backend.routes.equipment_routes import equipment_bp
from backend.routes.team_routes import team_bp
from backend.routes.technician_routes import technician_bp
from backend.routes.request_routes import request_bp
from backend.routes.dashboard_routes import dashboard_bp
from backend.routes.preventive_routes import preventive_bp
from backend.routes.auth_routes import auth_bp

def create_app(config_name='default'):
    """Application factory"""
    # Ensure project root is on sys.path so `import backend.*` works
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    # Serve frontend from the absolute frontend folder
    frontend_folder = os.path.join(base_dir, 'frontend')
    app = Flask(__name__, static_folder=frontend_folder, static_url_path='')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Set secret key for sessions
    app.secret_key = secrets.token_hex(32)
    
    # Initialize database connection
    db.init_app(app)
    
    # Enable CORS with credentials support
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints
    api_prefix = app.config['API_PREFIX']
    app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}')
    app.register_blueprint(equipment_bp, url_prefix=f'{api_prefix}')
    app.register_blueprint(team_bp, url_prefix=f'{api_prefix}')
    app.register_blueprint(technician_bp, url_prefix=f'{api_prefix}')
    app.register_blueprint(request_bp, url_prefix=f'{api_prefix}')
    app.register_blueprint(dashboard_bp, url_prefix=f'{api_prefix}')
    app.register_blueprint(preventive_bp, url_prefix=f'{api_prefix}')
    
    # Serve frontend files
    # Serve frontend files
    @app.route('/')
    def index():
        # Redirect to login page
        return send_from_directory(app.static_folder, 'login.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'login.html')
    
    # API health check
    @app.route(f'{api_prefix}/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'app': app.config['APP_NAME'],
            'version': app.config['VERSION']
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting GearGuard Admin Panel")
    print("=" * 60)
    
    app = create_app('development')
    
    print(f"\n✅ Server running at: http://localhost:5000")
    print(f"📊 Dashboard: http://localhost:5000/index.html")
    print(f"🔧 API Endpoint: http://localhost:5000/api")
    print(f"\n💡 Press CTRL+C to stop the server\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
