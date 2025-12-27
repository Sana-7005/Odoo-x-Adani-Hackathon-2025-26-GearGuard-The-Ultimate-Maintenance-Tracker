"""
Maintenance Request Model
Represents maintenance/repair requests for equipment
"""

from datetime import datetime
from backend.database.db import db

class MaintenanceRequest:
    """Maintenance Request model class"""
    
    @staticmethod
    def create(data):
        """Create new maintenance request"""
        query = """
            INSERT INTO maintenance_requests (equipment_id, team_id, technician_id, type, priority, status, description, requested_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        equipment_id = data.get('equipment_id')
        team_id = data.get('assigned_team_id')
        technician_id = data.get('assigned_technician_id')
        req_type = data.get('type', 'Corrective').capitalize()
        priority = data.get('priority', 'Medium').capitalize()
        status = data.get('status', 'New').capitalize()
        description = data.get('description', 'Maintenance Request')
        requested_date = data.get('requested_date', datetime.now().strftime('%Y-%m-%d'))

        request_id = db.execute_query(query, (equipment_id, team_id, technician_id, req_type, priority, status, description, requested_date), fetch_all=False)

        return {
            'id': request_id,
            'equipment_id': equipment_id,
            'description': description,
            'type': req_type.lower(),
            'priority': priority.lower(),
            'status': status.lower(),
            'assigned_team_id': team_id,
            'assigned_technician_id': technician_id,
            'requested_date': requested_date,
            'notes': data.get('notes', '')
        }
    
    @staticmethod
    def get_all():
        """Get all maintenance requests"""
        query = """
            SELECT id, equipment_id, team_id AS assigned_team_id, technician_id AS assigned_technician_id, 
                   type, priority, status, description, requested_date
            FROM maintenance_requests
            ORDER BY requested_date DESC
        """
        requests = db.execute_query(query)
        for req in requests:
            req['type'] = req.get('type', '').lower()
            req['priority'] = req.get('priority', 'medium').lower()
            req['status'] = req.get('status', 'new').lower().replace(' ', '_')
            req['notes'] = req.get('notes', '')
        return requests
    
    @staticmethod
    def get_by_id(request_id):
        """Get request by ID"""
        query = """
            SELECT id, equipment_id, team_id AS assigned_team_id, technician_id AS assigned_technician_id,
                   type, priority, status, description, requested_date
            FROM maintenance_requests
            WHERE id = %s
        """
        req = db.execute_query(query, (request_id,), fetch_one=True)
        if req:
            req['type'] = req.get('type', '').lower()
            req['priority'] = req.get('priority', 'medium').lower()
            req['status'] = req.get('status', 'new').lower().replace(' ', '_')
            req['notes'] = req.get('notes', '')
        return req
    
    @staticmethod
    def update(request_id, data):
        """Update maintenance request"""
        query = """
            UPDATE maintenance_requests
            SET equipment_id = %s, team_id = %s, technician_id = %s, type = %s, priority = %s, status = %s, description = %s
            WHERE id = %s
        """
        equipment_id = data.get('equipment_id')
        team_id = data.get('assigned_team_id')
        technician_id = data.get('assigned_technician_id')
        req_type = data.get('type', 'Corrective').capitalize()
        priority = data.get('priority', 'Medium').capitalize()
        status = data.get('status', 'New').capitalize()
        description = data.get('description')

        db.execute_query(query, (equipment_id, team_id, technician_id, req_type, priority, status, description, request_id), fetch_all=False)
        return MaintenanceRequest.get_by_id(request_id)
    
    @staticmethod
    def delete(request_id):
        """Delete maintenance request"""
        query = "DELETE FROM maintenance_requests WHERE id = %s"
        db.execute_query(query, (request_id,), fetch_all=False)
        return True
    
    @staticmethod
    def get_by_equipment(equipment_id):
        """Get requests for specific equipment"""
        query = """
            SELECT id, equipment_id, team_id AS assigned_team_id, type, priority, status, description, requested_date
            FROM maintenance_requests
            WHERE equipment_id = %s
        """
        requests = db.execute_query(query, (equipment_id,))
        for req in requests:
            req['type'] = req.get('type', '').lower()
            req['priority'] = req.get('priority', 'medium').lower()
            req['status'] = req.get('status', 'new').lower().replace(' ', '_')
            req['notes'] = req.get('notes', '')
        return requests
    
    @staticmethod
    def get_by_status(status):
        """Get requests by status"""
        # Map status to stage
        status_map = {
            'new': 'New',
            'in_progress': 'In Progress',
            'repaired': 'Repaired',
            'scrap': 'Scrap'
        }
        stage = status_map.get(status, 'New')
        
        query = """
            SELECT id, equipment_id, team_id AS assigned_team_id, type, priority, status, description, requested_date
            FROM maintenance_requests
            WHERE LOWER(status) = %s
        """
        requests = db.execute_query(query, (status.lower(),))
        for req in requests:
            req['type'] = req.get('type', '').lower()
            req['priority'] = req.get('priority', 'medium').lower()
            req['status'] = req.get('status', 'new').lower().replace(' ', '_')
            req['notes'] = req.get('notes', '')
        return requests
    
    @staticmethod
    def get_by_type(request_type):
        """Get requests by type"""
        query = """
            SELECT id, equipment_id, team_id AS assigned_team_id, type, priority, status, description, requested_date
            FROM maintenance_requests
            WHERE LOWER(type) = %s
        """
        requests = db.execute_query(query, (request_type.lower(),))
        for req in requests:
            req['type'] = req.get('type', '').lower()
            req['priority'] = req.get('priority', 'medium').lower()
            req['status'] = req.get('status', 'new').lower().replace(' ', '_')
            req['notes'] = req.get('notes', '')
        return requests
    
    @staticmethod
    def count_by_status():
        """Count requests by status"""
        query = """
            SELECT 
                SUM(CASE WHEN LOWER(status) = 'new' THEN 1 ELSE 0 END) as new,
                SUM(CASE WHEN LOWER(status) = 'in progress' THEN 1 ELSE 0 END) as in_progress,
                SUM(CASE WHEN LOWER(status) = 'repaired' THEN 1 ELSE 0 END) as repaired,
                SUM(CASE WHEN LOWER(status) = 'scrap' THEN 1 ELSE 0 END) as scrap
            FROM maintenance_requests
        """
        result = db.execute_query(query, fetch_one=True)
        return {
            'new': result['new'] or 0,
            'in_progress': result['in_progress'] or 0,
            'repaired': result['repaired'] or 0,
            'scrap': result['scrap'] or 0
        }
    
    @staticmethod
    def get_open_requests():
        """Get all open (new + in_progress) requests"""
        query = """
            SELECT id, equipment_id, team_id AS assigned_team_id, type, priority, status, description, requested_date
            FROM maintenance_requests
            WHERE LOWER(status) IN ('new', 'in progress')
        """
        requests = db.execute_query(query)
        for req in requests:
            req['asset_id'] = req['equipment_id']
            req['subject'] = req['description']
            req['request_type'] = req['type']
            req['stage'] = req['status']
            if req['status'] == 'in progress':
                req['status'] = 'in_progress'
            req['priority'] = req.get('priority', 'medium')
            req['completion_date'] = None
            req['notes'] = ''
        return requests
