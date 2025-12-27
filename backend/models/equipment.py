"""
Equipment Model
Represents physical assets/equipment in the maintenance system
"""

from backend.database.db import db

class Equipment:
    """Equipment model class"""
    
    @staticmethod
    def create(data):
        """Create new equipment"""
        query = """
            INSERT INTO equipment (name, type, department, purchase_date, warranty_expiry, status, default_team_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        name = data.get('name')
        type_ = data.get('type', 'General')
        department = data.get('department')
        purchase_date = data.get('purchase_date')
        warranty_expiry = data.get('warranty_expiry') or data.get('warranty')
        team_id = data.get('assigned_team_id')
        status = data.get('status', 'Active').capitalize()

        equipment_id = db.execute_query(query, (name, type_, department, purchase_date, warranty_expiry, status, team_id), fetch_all=False)

        return {
            'id': equipment_id,
            'name': name,
            'type': type_,
            'category': type_,
            'department': department,
            'purchase_date': purchase_date,
            'warranty_expiry': warranty_expiry,
            'warranty': warranty_expiry,
            'assigned_team_id': team_id,
            'status': status.lower(),
            'last_maintenance': data.get('last_maintenance')
        }
    
    @staticmethod
    def get_all():
        """Get all equipment"""
        query = """
            SELECT id, name, type, department, purchase_date, warranty_expiry, default_team_id AS assigned_team_id,
                   LOWER(status) as status
            FROM equipment
            WHERE status != 'Scrap'
        """
        equipment = db.execute_query(query)
        for eq in equipment:
            eq['category'] = eq.get('type')
            eq['warranty'] = eq.get('warranty_expiry')
            eq['last_maintenance'] = eq.get('last_maintenance', None)
        return equipment
    
    @staticmethod
    def get_by_id(equipment_id):
        """Get equipment by ID"""
        query = """
            SELECT id, name, type, department, purchase_date, warranty_expiry, default_team_id AS assigned_team_id,
                   LOWER(status) as status
            FROM equipment
            WHERE id = %s
        """
        eq = db.execute_query(query, (equipment_id,), fetch_one=True)
        if eq:
            eq['category'] = eq.get('type')
            eq['warranty'] = eq.get('warranty_expiry')
            eq['last_maintenance'] = eq.get('last_maintenance')
        return eq
    
    @staticmethod
    def update(equipment_id, data):
        """Update equipment"""
        query = """
            UPDATE equipment
            SET name = %s, type = %s, department = %s, purchase_date = %s, warranty_expiry = %s, default_team_id = %s, status = %s
            WHERE id = %s
        """
        name = data.get('name')
        type_ = data.get('type', data.get('category'))
        department = data.get('department')
        purchase_date = data.get('purchase_date')
        warranty_expiry = data.get('warranty') or data.get('warranty_expiry')
        team_id = data.get('assigned_team_id')
        status = data.get('status', 'Active').capitalize()

        db.execute_query(query, (name, type_, department, purchase_date, warranty_expiry, team_id, status, equipment_id), fetch_all=False)
        return Equipment.get_by_id(equipment_id)
    
    @staticmethod
    def delete(equipment_id):
        """Delete equipment (soft delete - mark as Scrapped)"""
        query = "UPDATE equipment SET status = 'Scrap' WHERE id = %s"
        db.execute_query(query, (equipment_id,), fetch_all=False)
        return True
    
    @staticmethod
    def get_by_status(status):
        """Get equipment by status"""
        query = """
            SELECT id, name, type, department, purchase_date, warranty_expiry, default_team_id AS assigned_team_id,
                   LOWER(status) as status
            FROM equipment
            WHERE LOWER(status) = %s
        """
        equipment = db.execute_query(query, (status.lower(),))
        for eq in equipment:
            eq['category'] = eq.get('type')
            eq['warranty'] = eq.get('warranty_expiry')
            eq['last_maintenance'] = eq.get('last_maintenance')
        return equipment
    
    @staticmethod
    def get_by_team(team_id):
        """Get equipment assigned to a team"""
        query = """
            SELECT id, name, type, department, purchase_date, warranty_expiry, default_team_id AS assigned_team_id,
                   LOWER(status) as status
            FROM equipment
            WHERE default_team_id = %s
        """
        equipment = db.execute_query(query, (team_id,))
        for eq in equipment:
            eq['category'] = eq.get('type')
            eq['warranty'] = eq.get('warranty_expiry')
            eq['last_maintenance'] = eq.get('last_maintenance')
        return equipment
    
    @staticmethod
    def count_by_status():
        """Count equipment by status"""
        query = """
            SELECT 
                SUM(CASE WHEN LOWER(status) = 'active' THEN 1 ELSE 0 END) as operational,
                SUM(CASE WHEN LOWER(status) = 'maintenance' THEN 1 ELSE 0 END) as maintenance,
                SUM(CASE WHEN LOWER(status) = 'breakdown' THEN 1 ELSE 0 END) as breakdown,
                SUM(CASE WHEN LOWER(status) = 'scrap' THEN 1 ELSE 0 END) as scrap
            FROM equipment
        """
        result = db.execute_query(query, fetch_one=True)
        return {
            'operational': result['operational'] or 0,
            'maintenance': result['maintenance'] or 0,
            'breakdown': result['breakdown'] or 0,
            'scrap': result['scrap'] or 0
        }
