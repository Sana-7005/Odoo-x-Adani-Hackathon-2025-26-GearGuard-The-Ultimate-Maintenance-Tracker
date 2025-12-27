"""
Preventive Schedule Routes
API endpoints for preventive maintenance scheduling
"""

from flask import Blueprint, request, jsonify
from backend.services.scheduling_service import SchedulingService

preventive_bp = Blueprint('preventive', __name__)

@preventive_bp.route('/preventive-schedules', methods=['GET'])
def get_all_schedules():
    """Get all preventive schedules"""
    try:
        schedules = SchedulingService.get_all_schedules()
        return jsonify({
            'success': True,
            'data': schedules
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@preventive_bp.route('/preventive-schedules/<int:schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    """Get specific preventive schedule"""
    try:
        schedule = SchedulingService.get_schedule_details(schedule_id)
        if not schedule:
            return jsonify({
                'success': False,
                'error': 'Schedule not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': schedule
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@preventive_bp.route('/preventive-schedules', methods=['POST'])
def create_schedule():
    """Create new preventive schedule"""
    try:
        data = request.get_json()
        schedule, error = SchedulingService.create_schedule(data)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': schedule
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@preventive_bp.route('/preventive-schedules/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    """Update preventive schedule"""
    try:
        data = request.get_json()
        schedule, error = SchedulingService.update_schedule(schedule_id, data)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 404
        
        return jsonify({
            'success': True,
            'data': schedule
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@preventive_bp.route('/preventive-schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    """Delete preventive schedule"""
    try:
        success, error = SchedulingService.delete_schedule(schedule_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': error
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Schedule deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@preventive_bp.route('/preventive-schedules/<int:schedule_id>/complete', methods=['POST'])
def complete_schedule(schedule_id):
    """Mark schedule as completed"""
    try:
        schedule, error = SchedulingService.complete_schedule(schedule_id)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 404
        
        return jsonify({
            'success': True,
            'data': schedule,
            'message': 'Schedule marked as completed'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@preventive_bp.route('/preventive-schedules/statistics', methods=['GET'])
def get_statistics():
    """Get preventive schedule statistics"""
    try:
        stats = SchedulingService.get_schedule_statistics()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@preventive_bp.route('/preventive-schedules/calendar', methods=['GET'])
def get_calendar():
    """Get calendar view of schedules"""
    try:
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        calendar_data = SchedulingService.get_calendar_view(year, month)
        
        return jsonify({
            'success': True,
            'data': calendar_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
