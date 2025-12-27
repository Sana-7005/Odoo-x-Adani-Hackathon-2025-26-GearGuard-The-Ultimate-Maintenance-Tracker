"""
Equipment Routes
API endpoints for equipment management
"""

from flask import Blueprint, request, jsonify
from backend.services.equipment_service import EquipmentService

equipment_bp = Blueprint('equipment', __name__)

@equipment_bp.route('/equipment', methods=['GET'])
def get_all_equipment():
    """Get all equipment"""
    try:
        equipment = EquipmentService.get_all_equipment()
        return jsonify({
            'success': True,
            'data': equipment
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@equipment_bp.route('/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment(equipment_id):
    """Get single equipment with details"""
    try:
        equipment = EquipmentService.get_equipment_details(equipment_id)
        if not equipment:
            return jsonify({
                'success': False,
                'error': 'Equipment not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': equipment
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@equipment_bp.route('/equipment', methods=['POST'])
def create_equipment():
    """Create new equipment"""
    try:
        data = request.get_json()
        equipment, error = EquipmentService.create_equipment(data)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': equipment,
            'message': 'Equipment created successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@equipment_bp.route('/equipment/<int:equipment_id>', methods=['PUT'])
def update_equipment(equipment_id):
    """Update equipment"""
    try:
        data = request.get_json()
        equipment, error = EquipmentService.update_equipment(equipment_id, data)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 404
        
        return jsonify({
            'success': True,
            'data': equipment,
            'message': 'Equipment updated successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@equipment_bp.route('/equipment/<int:equipment_id>', methods=['DELETE'])
def delete_equipment(equipment_id):
    """Delete equipment"""
    try:
        success, error = EquipmentService.delete_equipment(equipment_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Equipment deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@equipment_bp.route('/equipment/statistics', methods=['GET'])
def get_equipment_statistics():
    """Get equipment statistics"""
    try:
        stats = EquipmentService.get_equipment_statistics()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
