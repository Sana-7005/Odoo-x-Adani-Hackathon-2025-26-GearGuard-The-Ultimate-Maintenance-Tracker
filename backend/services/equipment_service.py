"""
Equipment Service
Business logic for equipment management
"""

from backend.models.equipment import Equipment
from backend.models.maintenance_request import MaintenanceRequest

class EquipmentService:
    """Equipment service class"""
    
    @staticmethod
    def get_all_equipment():
        """Get all equipment with additional info"""
        equipment_list = Equipment.get_all()
        
        # Add open request count for each equipment
        for equipment in equipment_list:
            open_requests = [r for r in MaintenanceRequest.get_by_equipment(equipment.get('id')) 
                           if r.get('status') in ['new', 'in_progress']]
            equipment['open_requests_count'] = len(open_requests)
        
        return equipment_list
    
    @staticmethod
    def get_equipment_details(equipment_id):
        """Get equipment with full details"""
        equipment = Equipment.get_by_id(equipment_id)
        if not equipment:
            return None
        
        # Add maintenance history
        requests = MaintenanceRequest.get_by_equipment(equipment_id)
        equipment['maintenance_history'] = requests
        equipment['total_requests'] = len(requests)
        equipment['open_requests'] = [r for r in requests if r['status'] in ['new', 'in_progress']]
        
        return equipment
    
    @staticmethod
    def create_equipment(data):
        """Create new equipment"""
        # Validate required fields
        required = ['name', 'type', 'department', 'assigned_team_id', 'purchase_date']
        for field in required:
            if not data.get(field):
                return None, f"Missing required field: {field}"
        
        equipment = Equipment.create(data)
        return equipment, None
    
    @staticmethod
    def update_equipment(equipment_id, data):
        """Update equipment"""
        equipment = Equipment.update(equipment_id, data)
        if not equipment:
            return None, "Equipment not found"
        return equipment, None
    
    @staticmethod
    def delete_equipment(equipment_id):
        """Delete equipment"""
        # Check if equipment has open requests
        open_requests = [r for r in MaintenanceRequest.get_by_equipment(equipment_id) 
                        if r['status'] in ['new', 'in_progress']]
        
        if open_requests:
            return False, "Cannot delete equipment with open maintenance requests"
        
        success = Equipment.delete(equipment_id)
        if not success:
            return False, "Equipment not found"
        
        return True, None
    
    @staticmethod
    def get_equipment_statistics():
        """Get equipment statistics"""
        all_equipment = Equipment.get_all()
        status_counts = Equipment.count_by_status()
        
        return {
            'total': len(all_equipment),
            'by_status': status_counts,
            'operational_percentage': round((status_counts['operational'] / len(all_equipment) * 100) if all_equipment else 0, 1)
        }
