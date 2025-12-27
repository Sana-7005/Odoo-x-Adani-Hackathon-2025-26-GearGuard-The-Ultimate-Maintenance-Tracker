"""
Request Routes
API endpoints for maintenance request management
"""

from flask import Blueprint, request, jsonify
from backend.services.request_service import RequestService

request_bp = Blueprint('request', __name__)

@request_bp.route('/requests', methods=['GET'])
def get_all_requests():
    """Get all maintenance requests"""
    try:
        requests = RequestService.get_all_requests()
        return jsonify({
            'success': True,
            'data': requests
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@request_bp.route('/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    """Get single request with details"""
    try:
        req = RequestService.get_request_details(request_id)
        if not req:
            return jsonify({
                'success': False,
                'error': 'Request not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': req
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@request_bp.route('/requests', methods=['POST'])
def create_request():
    """Create new maintenance request"""
    try:
        data = request.get_json()
        req, error = RequestService.create_request(data)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': req,
            'message': 'Request created successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@request_bp.route('/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    """Update maintenance request"""
    try:
        data = request.get_json()
        req, error = RequestService.update_request(request_id, data)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 404
        
        return jsonify({
            'success': True,
            'data': req,
            'message': 'Request updated successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@request_bp.route('/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    """Delete maintenance request"""
    try:
        success, error = RequestService.delete_request(request_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': error
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Request deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@request_bp.route('/requests/statistics', methods=['GET'])
def get_request_statistics():
    """Get request statistics"""
    try:
        stats = RequestService.get_request_statistics()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@request_bp.route('/requests/<int:request_id>/assign', methods=['POST'])
def assign_technician(request_id):
    """Assign technician to request"""
    try:
        data = request.get_json()
        technician_id = data.get('technician_id')
        
        if not technician_id:
            return jsonify({
                'success': False,
                'error': 'Missing technician_id'
            }), 400
        
        req, error = RequestService.assign_technician(request_id, technician_id)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 404
        
        return jsonify({
            'success': True,
            'data': req,
            'message': 'Technician assigned successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
