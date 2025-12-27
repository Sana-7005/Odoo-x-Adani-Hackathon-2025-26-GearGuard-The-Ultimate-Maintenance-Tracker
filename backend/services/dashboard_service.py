"""
Dashboard Service
Business logic for dashboard analytics and statistics
"""

from backend.models.equipment import Equipment
from backend.models.team import Team
from backend.models.technician import Technician
from backend.models.maintenance_request import MaintenanceRequest
from backend.models.preventive_schedule import PreventiveSchedule
from backend.services.equipment_service import EquipmentService
from backend.services.request_service import RequestService
from backend.services.scheduling_service import SchedulingService
from datetime import datetime, timedelta

class DashboardService:
    """Dashboard service class"""
    
    @staticmethod
    def get_overview_stats():
        """Get overview statistics for dashboard"""
        equipment_stats = EquipmentService.get_equipment_statistics()
        request_stats = RequestService.get_request_statistics()
        schedule_stats = SchedulingService.get_schedule_statistics()
        
        return {
            'equipment': equipment_stats,
            'requests': request_stats,
            'schedules': schedule_stats,
            'teams': {
                'total': len(Team.get_all())
            },
            'technicians': {
                'total': len(Technician.get_all()),
                'active': len(Technician.get_by_status('active'))
            }
        }
    
    @staticmethod
    def get_recent_activities():
        """Get recent maintenance activities"""
        # Get recent requests (last 10)
        all_requests = MaintenanceRequest.get_all()
        sorted_requests = sorted(all_requests, 
                               key=lambda x: x['requested_date'], 
                               reverse=True)[:10]
        
        activities = []
        for request in sorted_requests:
            equipment = Equipment.get_by_id(request['equipment_id'])
            activities.append({
                'type': 'request',
                'id': request['id'],
                'title': f"Maintenance request for {equipment['name'] if equipment else 'Unknown'}",
                'status': request['status'],
                'priority': request['priority'],
                'date': request['requested_date']
            })
        
        return activities
    
    @staticmethod
    def get_critical_alerts():
        """Get critical alerts that need attention"""
        alerts = []
        
        # Critical priority requests
        critical_requests = [r for r in MaintenanceRequest.get_all() 
                           if r['priority'] == 'critical' and r['status'] in ['new', 'in_progress']]
        
        for request in critical_requests:
            equipment = Equipment.get_by_id(request['equipment_id'])
            alerts.append({
                'type': 'critical_request',
                'severity': 'critical',
                'message': f"Critical maintenance needed: {equipment['name'] if equipment else 'Unknown'}",
                'details': request['description'],
                'id': request['id']
            })
        
        # Overdue preventive maintenance
        overdue_schedules = PreventiveSchedule.get_overdue()
        for schedule in overdue_schedules[:5]:  # Limit to 5
            equipment = Equipment.get_by_id(schedule['equipment_id'])
            alerts.append({
                'type': 'overdue_maintenance',
                'severity': 'high',
                'message': f"Overdue preventive maintenance: {equipment['name'] if equipment else 'Unknown'}",
                'details': schedule['task_name'],
                'id': schedule['id']
            })
        
        # Equipment in breakdown status
        breakdown_equipment = Equipment.get_by_status('breakdown')
        for equipment in breakdown_equipment:
            alerts.append({
                'type': 'equipment_breakdown',
                'severity': 'critical',
                'message': f"Equipment breakdown: {equipment['name']}",
                'details': f"Type: {equipment['type']}, Department: {equipment['department']}",
                'id': equipment['id']
            })
        
        return alerts
    
    @staticmethod
    def get_team_performance():
        """Get team performance metrics"""
        teams = Team.get_all()
        performance = []
        
        for team in teams:
            team_requests = [r for r in MaintenanceRequest.get_all() 
                           if r['assigned_team_id'] == team['id']]
            
            completed = len([r for r in team_requests if r['status'] == 'repaired'])
            open_count = len([r for r in team_requests if r['status'] in ['new', 'in_progress']])
            
            performance.append({
                'team_id': team['id'],
                'team_name': team['name'],
                'total_requests': len(team_requests),
                'completed': completed,
                'open': open_count,
                'completion_rate': round((completed / len(team_requests) * 100) if team_requests else 0, 1),
                'technician_count': Team.count_technicians(team['id'])
            })
        
        return performance
    
    @staticmethod
    def get_equipment_status_distribution():
        """Get equipment status distribution for charts"""
        status_counts = Equipment.count_by_status()
        
        return [
            {'status': 'Operational', 'count': status_counts['operational'], 'color': '#10b981'},
            {'status': 'Maintenance', 'count': status_counts['maintenance'], 'color': '#f59e0b'},
            {'status': 'Breakdown', 'count': status_counts['breakdown'], 'color': '#ef4444'},
            {'status': 'Scrap', 'count': status_counts['scrap'], 'color': '#6b7280'}
        ]
    
    @staticmethod
    def get_request_trends(days=30):
        """Get maintenance request trends over time"""
        all_requests = MaintenanceRequest.get_all()
        today = datetime.now()
        trends = []
        
        for i in range(days, 0, -1):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            count = len([r for r in all_requests if r['requested_date'] == date])
            trends.append({
                'date': date,
                'count': count
            })
        
        return trends
    
    @staticmethod
    def get_upcoming_preventive_tasks():
        """Get upcoming preventive maintenance tasks (next 7 days)"""
        all_schedules = PreventiveSchedule.get_all()
        today = datetime.now()
        upcoming = []
        
        for schedule in all_schedules:
            try:
                due_date = datetime.strptime(schedule['next_due'], '%Y-%m-%d')
                days_until = (due_date - today).days
                
                if 0 <= days_until <= 7 and schedule['status'] != 'completed':
                    equipment = Equipment.get_by_id(schedule['equipment_id'])
                    upcoming.append({
                        'id': schedule['id'],
                        'task': schedule['task_name'],
                        'equipment': equipment['name'] if equipment else 'Unknown',
                        'due_date': schedule['next_due'],
                        'days_until': days_until,
                        'status': schedule['status']
                    })
            except:
                pass
        
        # Sort by days_until
        upcoming.sort(key=lambda x: x['days_until'])
        
        return upcoming
