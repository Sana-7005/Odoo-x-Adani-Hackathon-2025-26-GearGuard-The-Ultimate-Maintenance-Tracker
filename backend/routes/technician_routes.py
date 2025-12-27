"""
Technician Routes
API endpoints for technician management
"""

from flask import Blueprint, request, jsonify
from backend.models.technician import Technician

technician_bp = Blueprint('technician', __name__)

@technician_bp.route('/technicians', methods=['GET'])
def get_all_technicians():
    """Get all technicians"""
    try:
        technicians = Technician.get_all()
        return jsonify({
            'success': True,
            'data': technicians
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@technician_bp.route('/technicians/<int:technician_id>', methods=['GET'])
def get_technician(technician_id):
    """Get single technician"""
    try:
        technician = Technician.get_by_id(technician_id)
        if not technician:
            return jsonify({
                'success': False,
                'error': 'Technician not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': technician
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@technician_bp.route('/technicians', methods=['POST'])
def create_technician():
    """Create new technician"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['name', 'email', 'phone', 'team_id']
        for field in required:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        technician = Technician.create(data)
        
        return jsonify({
            'success': True,
            'data': technician,
            'message': 'Technician created successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@technician_bp.route('/technicians/<int:technician_id>', methods=['PUT'])
def update_technician(technician_id):
    """Update technician"""
    try:
        data = request.get_json()
        technician = Technician.update(technician_id, data)
        
        if not technician:
            return jsonify({
                'success': False,
                'error': 'Technician not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': technician,
            'message': 'Technician updated successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@technician_bp.route('/technicians/<int:technician_id>', methods=['DELETE'])
def delete_technician(technician_id):
    """Delete technician"""
    try:
        success = Technician.delete(technician_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Technician not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Technician deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@technician_bp.route('/technicians/team/<int:team_id>', methods=['GET'])
def get_technicians_by_team(team_id):
    """Get technicians by team"""
    try:
        technicians = Technician.get_by_team(team_id)
        return jsonify({
            'success': True,
            'data': technicians
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
