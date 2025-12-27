"""
Request Service
Business logic for maintenance request management
"""

from backend.models.maintenance_request import MaintenanceRequest
from backend.models.equipment import Equipment
from backend.models.team import Team
from backend.models.technician import Technician
from datetime import datetime

class RequestService:
    """Request service class"""
    
    @staticmethod
    def get_all_requests():
        """Get all maintenance requests with equipment info"""
        requests = MaintenanceRequest.get_all()
        
        # Enrich with equipment details
        for request in requests:
            equipment = Equipment.get_by_id(request.get('equipment_id'))
            if equipment:
                request['equipment_name'] = equipment.get('name', 'Unknown')
                request['equipment_type'] = equipment.get('type', 'Unknown')
            else:
                request['equipment_name'] = 'Unknown'
                request['equipment_type'] = 'Unknown'
            # Enrich with assigned team and technician names when available
            team = Team.get_by_id(request.get('assigned_team_id')) if request.get('assigned_team_id') else None
            tech = Technician.get_by_id(request.get('assigned_technician_id')) if request.get('assigned_technician_id') else None
            request['assigned_team_name'] = team.get('name') if team else None
            request['assigned_technician_name'] = tech.get('name') if tech else None
        
        return requests
    
    @staticmethod
    def get_request_details(request_id):
        """Get request with full details"""
        request = MaintenanceRequest.get_by_id(request_id)
        if not request:
            return None
        
        # Add equipment details
        equipment = Equipment.get_by_id(request['equipment_id'])
        if equipment:
            request['equipment'] = equipment
        # Add team and technician details
        if request.get('assigned_team_id'):
            team = Team.get_by_id(request.get('assigned_team_id'))
            if team:
                request['assigned_team'] = team
        if request.get('assigned_technician_id'):
            tech = Technician.get_by_id(request.get('assigned_technician_id'))
            if tech:
                request['assigned_technician'] = tech
        
        return request
    
    @staticmethod
    def create_request(data):
        """Create new maintenance request"""
        # Validate required fields
        required = ['equipment_id', 'type', 'priority', 'description']
        for field in required:
            if not data.get(field):
                return None, f"Missing required field: {field}"
        
        # Auto-assign team based on equipment
        equipment = Equipment.get_by_id(data['equipment_id'])
        if equipment:
            data['assigned_team_id'] = equipment['assigned_team_id']

        # If technician provided, ensure it's keyed correctly
        if data.get('assigned_technician_id'):
            data['assigned_technician_id'] = data.get('assigned_technician_id')
        
        # Update equipment status if corrective request
        if data['type'] == 'corrective' and equipment:
            if equipment['status'] == 'operational':
                Equipment.update(equipment['id'], {'status': 'maintenance'})
        
        request = MaintenanceRequest.create(data)
        return request, None
    
    @staticmethod
    def update_request(request_id, data):
        """Update maintenance request"""
        old_request = MaintenanceRequest.get_by_id(request_id)
        if not old_request:
            return None, "Request not found"
        
        # Handle status changes
        new_status = data.get('status')
        if new_status and new_status != old_request['status']:
            equipment = Equipment.get_by_id(old_request['equipment_id'])
            
            if new_status == 'repaired':
                # Mark equipment as operational
                if equipment:
                    Equipment.update(equipment['id'], {
                        'status': 'operational',
                        'last_maintenance': datetime.now().strftime('%Y-%m-%d')
                    })
            
            elif new_status == 'scrap':
                # Mark equipment as scrap
                if equipment:
                    Equipment.update(equipment['id'], {'status': 'scrap'})
        
        request = MaintenanceRequest.update(request_id, data)
        return request, None
    
    @staticmethod
    def delete_request(request_id):
        """Delete maintenance request"""
        success = MaintenanceRequest.delete(request_id)
        if not success:
            return False, "Request not found"
        return True, None
    
    @staticmethod
    def get_request_statistics():
        """Get request statistics"""
        all_requests = MaintenanceRequest.get_all()
        status_counts = MaintenanceRequest.count_by_status()
        open_requests = MaintenanceRequest.get_open_requests()
        
        corrective = len(MaintenanceRequest.get_by_type('corrective'))
        preventive = len(MaintenanceRequest.get_by_type('preventive'))
        
        return {
            'total': len(all_requests),
            'open': len(open_requests),
            'by_status': status_counts,
            'by_type': {
                'corrective': corrective,
                'preventive': preventive
            }
        }
    
    @staticmethod
    def assign_technician(request_id, technician_id):
        """Assign technician to request"""
        request = MaintenanceRequest.get_by_id(request_id)
        if not request:
            return None, "Request not found"
        
        data = {'assigned_technician_id': technician_id}
        if request['status'] == 'new':
            data['status'] = 'in_progress'
        
        return MaintenanceRequest.update(request_id, data), None
