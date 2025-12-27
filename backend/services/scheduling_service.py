"""
Scheduling Service
Business logic for preventive maintenance scheduling
"""

from backend.models.preventive_schedule import PreventiveSchedule
from backend.models.equipment import Equipment
from datetime import datetime, timedelta

class SchedulingService:
    """Scheduling service class"""
    
    @staticmethod
    def get_all_schedules():
        """Get all preventive schedules with equipment info"""
        schedules = PreventiveSchedule.get_all()
        
        # Enrich with equipment details
        for schedule in schedules:
            equipment = Equipment.get_by_id(schedule['equipment_id'])
            if equipment:
                schedule['equipment_name'] = equipment.get('name', 'Unknown')
                schedule['equipment_type'] = equipment.get('type', 'Unknown')
            else:
                schedule['equipment_name'] = 'Unknown'
                schedule['equipment_type'] = 'Unknown'
            
            # Check if overdue
            schedule['is_overdue'] = SchedulingService._is_overdue(schedule.get('next_due'))
        
        return schedules
    
    @staticmethod
    def get_schedule_details(schedule_id):
        """Get schedule with full details"""
        schedule = PreventiveSchedule.get_by_id(schedule_id)
        if not schedule:
            return None
        
        # Add equipment details
        equipment = Equipment.get_by_id(schedule['equipment_id'])
        if equipment:
            schedule['equipment'] = equipment
        
        schedule['is_overdue'] = SchedulingService._is_overdue(schedule['next_due'])
        
        return schedule
    
    @staticmethod
    def create_schedule(data):
        """Create new preventive schedule"""
        # Validate required fields
        required = ['equipment_id', 'task_name', 'frequency', 'next_due']
        for field in required:
            if not data.get(field):
                return None, f"Missing required field: {field}"
        
        # Auto-assign team based on equipment
        equipment = Equipment.get_by_id(data['equipment_id'])
        if equipment:
            data['assigned_team_id'] = equipment['assigned_team_id']
        
        # Check if overdue
        if SchedulingService._is_overdue(data['next_due']):
            data['status'] = 'overdue'
        else:
            data['status'] = 'scheduled'
        
        schedule = PreventiveSchedule.create(data)
        return schedule, None
    
    @staticmethod
    def update_schedule(schedule_id, data):
        """Update preventive schedule"""
        schedule = PreventiveSchedule.update(schedule_id, data)
        if not schedule:
            return None, "Schedule not found"
        
        # Update overdue status
        if SchedulingService._is_overdue(schedule['next_due']):
            schedule['status'] = 'overdue'
        
        return schedule, None
    
    @staticmethod
    def delete_schedule(schedule_id):
        """Delete preventive schedule"""
        success = PreventiveSchedule.delete(schedule_id)
        if not success:
            return False, "Schedule not found"
        return True, None
    
    @staticmethod
    def complete_schedule(schedule_id):
        """Mark schedule as completed and calculate next due date"""
        schedule = PreventiveSchedule.get_by_id(schedule_id)
        if not schedule:
            return None, "Schedule not found"
        
        today = datetime.now().strftime('%Y-%m-%d')
        next_due = SchedulingService._calculate_next_due(today, schedule['frequency'])
        
        updated = PreventiveSchedule.update(schedule_id, {
            'last_completed': today,
            'next_due': next_due,
            'status': 'scheduled'
        })
        
        # Update equipment last maintenance date
        Equipment.update(schedule['equipment_id'], {'last_maintenance': today})
        
        return updated, None
    
    @staticmethod
    def get_schedule_statistics():
        """Get schedule statistics"""
        all_schedules = PreventiveSchedule.get_all()
        overdue = PreventiveSchedule.get_overdue()
        
        due_soon = []
        today = datetime.now()
        for schedule in all_schedules:
            due_date = datetime.strptime(schedule['next_due'], '%Y-%m-%d')
            days_until = (due_date - today).days
            if 0 < days_until <= 7 and schedule['status'] != 'completed':
                due_soon.append(schedule)
        
        return {
            'total': len(all_schedules),
            'overdue': len(overdue),
            'due_this_week': len(due_soon),
            'scheduled': len([s for s in all_schedules if s['status'] == 'scheduled'])
        }
    
    @staticmethod
    def get_calendar_view(year, month):
        """Get schedules for calendar view"""
        schedules = PreventiveSchedule.get_all()
        calendar_data = {}
        
        for schedule in schedules:
            date = schedule['next_due']
            if date not in calendar_data:
                calendar_data[date] = []
            
            equipment = Equipment.get_by_id(schedule['equipment_id'])
            calendar_data[date].append({
                'id': schedule['id'],
                'task': schedule['task_name'],
                'equipment': equipment['name'] if equipment else 'Unknown',
                'status': schedule['status']
            })
        
        return calendar_data
    
    @staticmethod
    def _is_overdue(due_date_str):
        """Check if a date is overdue"""
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            return due_date < datetime.now()
        except:
            return False
    
    @staticmethod
    def _calculate_next_due(current_date_str, frequency):
        """Calculate next due date based on frequency"""
        current = datetime.strptime(current_date_str, '%Y-%m-%d')
        
        if frequency == 'daily':
            next_date = current + timedelta(days=1)
        elif frequency == 'weekly':
            next_date = current + timedelta(weeks=1)
        elif frequency == 'monthly':
            next_date = current + timedelta(days=30)
        elif frequency == 'quarterly':
            next_date = current + timedelta(days=90)
        elif frequency == 'yearly':
            next_date = current + timedelta(days=365)
        else:
            next_date = current + timedelta(days=30)
        
        return next_date.strftime('%Y-%m-%d')
