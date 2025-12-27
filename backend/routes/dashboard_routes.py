"""
Dashboard Routes
API endpoints for dashboard analytics
"""

from flask import Blueprint, request, jsonify
from backend.services.dashboard_service import DashboardService
from backend.services.scheduling_service import SchedulingService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/overview', methods=['GET'])
def get_overview():
    """Get dashboard overview statistics"""
    try:
        stats = DashboardService.get_overview_stats()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/dashboard/activities', methods=['GET'])
def get_recent_activities():
    """Get recent activities"""
    try:
        activities = DashboardService.get_recent_activities()
        return jsonify({
            'success': True,
            'data': activities
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/dashboard/alerts', methods=['GET'])
def get_critical_alerts():
    """Get critical alerts"""
    try:
        alerts = DashboardService.get_critical_alerts()
        return jsonify({
            'success': True,
            'data': alerts
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/dashboard/teams/performance', methods=['GET'])
def get_team_performance():
    """Get team performance metrics"""
    try:
        performance = DashboardService.get_team_performance()
        return jsonify({
            'success': True,
            'data': performance
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/dashboard/equipment/status-distribution', methods=['GET'])
def get_equipment_status_distribution():
    """Get equipment status distribution"""
    try:
        distribution = DashboardService.get_equipment_status_distribution()
        return jsonify({
            'success': True,
            'data': distribution
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/dashboard/requests/trends', methods=['GET'])
def get_request_trends():
    """Get request trends"""
    try:
        days = request.args.get('days', default=30, type=int)
        trends = DashboardService.get_request_trends(days)
        return jsonify({
            'success': True,
            'data': trends
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/dashboard/preventive/upcoming', methods=['GET'])
def get_upcoming_preventive():
    """Get upcoming preventive tasks"""
    try:
        tasks = DashboardService.get_upcoming_preventive_tasks()
        return jsonify({
            'success': True,
            'data': tasks
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/preventive-schedules', methods=['GET'])
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

@dashboard_bp.route('/preventive-schedules', methods=['POST'])
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
            'data': schedule,
            'message': 'Schedule created successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/preventive-schedules/<int:schedule_id>', methods=['PUT'])
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
            'data': schedule,
            'message': 'Schedule updated successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/preventive-schedules/<int:schedule_id>', methods=['DELETE'])
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

@dashboard_bp.route('/preventive-schedules/<int:schedule_id>/complete', methods=['POST'])
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
