"""
Technician Model
Represents technicians/maintenance workers
"""

from backend.database.db import db

class Technician:
    """Technician model class"""
    
    @staticmethod
    def create(data):
        """Create new technician"""
        query = """
            INSERT INTO technicians (team_id, name, email, phone, skill_level, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        team_id = data.get('team_id')
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        skill_level = data.get('skill_level', 'Technician')
        status = data.get('status', 'Active')
        
        tech_id = db.execute_query(query, (team_id, name, email, phone, skill_level, status), fetch_all=False)
        
        return {
            'id': tech_id,
            'team_id': team_id,
            'name': name,
            'email': email,
            'phone': phone,
            'skill_level': skill_level,
            'status': status.lower()
        }
    
    @staticmethod
    def get_all():
        """Get all technicians"""
        query = """
            SELECT id, team_id, name, email, phone, skill_level, 
                   IFNULL(status, 'Active') as status
            FROM technicians
        """
        technicians = db.execute_query(query)
        for tech in technicians:
            tech['status'] = tech['status'].lower() if tech.get('status') else 'active'
        return technicians
    
    @staticmethod
    def get_by_id(technician_id):
        """Get technician by ID"""
        query = """
            SELECT id, team_id, name, email, phone, skill_level, 
                   IFNULL(status, 'Active') as status
            FROM technicians 
            WHERE id = %s
        """
        tech = db.execute_query(query, (technician_id,), fetch_one=True)
        if tech:
            tech['status'] = tech['status'].lower() if tech.get('status') else 'active'
        return tech
    
    @staticmethod
    def update(technician_id, data):
        """Update technician"""
        query = """
            UPDATE technicians 
            SET name = %s, skill_level = %s, phone = %s, email = %s, 
                team_id = %s, status = %s
            WHERE id = %s
        """
        name = data.get('name')
        skill_level = data.get('skill_level', 'Technician')
        phone = data.get('phone')
        email = data.get('email')
        team_id = data.get('team_id')
        status = data.get('status', 'Active').capitalize()
        
        db.execute_query(query, (name, skill_level, phone, email, team_id, status, technician_id), fetch_all=False)
        return Technician.get_by_id(technician_id)
    
    @staticmethod
    def delete(technician_id):
        """Delete technician"""
        query = "DELETE FROM technicians WHERE id = %s"
        db.execute_query(query, (technician_id,), fetch_all=False)
        return True
    
    @staticmethod
    def get_by_team(team_id):
        """Get technicians by team"""
        query = """
            SELECT id, team_id, name, email, phone, skill_level, 
                   IFNULL(status, 'Active') as status
            FROM technicians 
            WHERE team_id = %s
        """
        technicians = db.execute_query(query, (team_id,))
        for tech in technicians:
            tech['status'] = tech['status'].lower() if tech.get('status') else 'active'
        return technicians
    
    @staticmethod
    def get_by_status(status):
        """Get technicians by status"""
        query = """
            SELECT id, team_id, name, email, phone, skill_level, 
                   IFNULL(status, 'Active') as status
            FROM technicians 
            WHERE LOWER(status) = %s
        """
        technicians = db.execute_query(query, (status.lower(),))
        for tech in technicians:
            tech['status'] = tech['status'].lower() if tech.get('status') else 'active'
        return technicians
