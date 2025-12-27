"""
Team Model
Represents maintenance teams in the system
"""

from backend.database.db import db

class Team:
    """Team model class"""
    
    @staticmethod
    def create(data):
        """Create new team"""
        query = """
            INSERT INTO teams (company_id, name, type)
            VALUES (%s, %s, %s)
        """
        # Default to company_id=1 if not provided
        company_id = data.get('company_id', 1)
        team_name = data.get('name')
        team_type = data.get('type', 'Mechanical')
        
        team_id = db.execute_query(query, (company_id, team_name, team_type), fetch_all=False)
        
        return {
            'id': team_id,
            'company_id': company_id,
            'name': team_name,
            'type': team_type
        }
    
    @staticmethod
    def get_all():
        """Get all teams"""
        query = "SELECT id, company_id, name, type FROM teams"
        teams = db.execute_query(query)
        return teams
    
    @staticmethod
    def get_by_id(team_id):
        """Get team by ID"""
        query = "SELECT id, company_id, name, type FROM teams WHERE id = %s"
        team = db.execute_query(query, (team_id,), fetch_one=True)
        if team:
            team['department'] = team.get('department', '')
            team['specialization'] = team.get('specialization', '')
            team['team_name'] = team['name']
        return team
    
    @staticmethod
    def update(team_id, data):
        """Update team"""
        query = """
            UPDATE teams 
            SET name = %s, type = %s
            WHERE id = %s
        """
        team_name = data.get('name')
        team_type = data.get('type', 'Mechanical')
        
        db.execute_query(query, (team_name, team_type, team_id), fetch_all=False)
        return Team.get_by_id(team_id)
    
    @staticmethod
    def delete(team_id):
        """Delete team"""
        query = "DELETE FROM teams WHERE id = %s"
        db.execute_query(query, (team_id,), fetch_all=False)
        return True
    
    @staticmethod
    def get_technicians(team_id):
        """Get all technicians in a team"""
        query = """
            SELECT id, team_id, name, email, phone, skill_level, status
            FROM technicians 
            WHERE team_id = %s
        """
        return db.execute_query(query, (team_id,))
    
    @staticmethod
    def count_technicians(team_id):
        """Count technicians in a team"""
        query = "SELECT COUNT(*) as count FROM technicians WHERE team_id = %s"
        result = db.execute_query(query, (team_id,), fetch_one=True)
        return result['count'] if result else 0
