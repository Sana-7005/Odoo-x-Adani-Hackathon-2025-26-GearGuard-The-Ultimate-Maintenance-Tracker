"""
Team Routes
API endpoints for team management
"""

from flask import Blueprint, request, jsonify
from backend.models.team import Team

team_bp = Blueprint('team', __name__)

@team_bp.route('/teams', methods=['GET'])
def get_all_teams():
    """Get all teams"""
    try:
        teams = Team.get_all()
        
        # Add technician count for each team
        for team in teams:
            team['technician_count'] = Team.count_technicians(team['id'])
        
        return jsonify({
            'success': True,
            'data': teams
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@team_bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    """Get single team with details"""
    try:
        team = Team.get_by_id(team_id)
        if not team:
            return jsonify({
                'success': False,
                'error': 'Team not found'
            }), 404
        
        # Add technicians
        team['technicians'] = Team.get_technicians(team_id)
        team['technician_count'] = len(team['technicians'])
        
        return jsonify({
            'success': True,
            'data': team
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@team_bp.route('/teams', methods=['POST'])
def create_team():
    """Create new team"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['name', 'department', 'specialization']
        for field in required:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        team = Team.create(data)
        
        return jsonify({
            'success': True,
            'data': team,
            'message': 'Team created successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@team_bp.route('/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    """Update team"""
    try:
        data = request.get_json()
        team = Team.update(team_id, data)
        
        if not team:
            return jsonify({
                'success': False,
                'error': 'Team not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': team,
            'message': 'Team updated successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@team_bp.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    """Delete team"""
    try:
        # Check if team has technicians
        if Team.count_technicians(team_id) > 0:
            return jsonify({
                'success': False,
                'error': 'Cannot delete team with assigned technicians'
            }), 400
        
        success = Team.delete(team_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Team not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Team deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
