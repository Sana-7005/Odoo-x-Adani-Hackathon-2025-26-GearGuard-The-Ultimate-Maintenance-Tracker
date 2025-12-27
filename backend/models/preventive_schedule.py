"""
Preventive Schedule Model
Represents scheduled preventive maintenance tasks
Uses MySQL database via maintenance_jobs table with preventive request_type
"""

from datetime import datetime
from backend.database.db import db

class PreventiveSchedule:
    """Preventive Schedule model class"""
    
    @staticmethod
    def create(data):
        """Create new preventive schedule"""
        query = """
            INSERT INTO preventive_schedules (equipment_id, task, frequency, next_due, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        equipment_id = data.get('equipment_id')
        task_name = data.get('task_name', 'Preventive Maintenance')
        frequency = data.get('frequency', 'Monthly').capitalize()
        next_due = data.get('next_due')
        status = data.get('status', 'Active').capitalize()
        
        schedule_id = db.execute_query(query, (equipment_id, task_name, frequency, next_due, status), 
                                      fetch_all=False)
        
        return {
            'id': schedule_id,
            'equipment_id': equipment_id,
            'task_name': task_name,
            'frequency': frequency,
            'last_completed': data.get('last_completed'),
            'next_due': next_due,
            'status': status.lower()
        }
    
    @staticmethod
    def get_all():
        """Get all preventive schedules"""
        query = """
            SELECT id, equipment_id, task AS task_name, frequency, next_due, LOWER(status) as status
            FROM preventive_schedules
        """
        schedules = db.execute_query(query)
        for schedule in schedules:
            schedule['frequency'] = schedule.get('frequency', 'Monthly')
            # Get last completed execution for this schedule
            try:
                res = db.execute_query("SELECT MAX(executed_on) as last_completed FROM preventive_executions WHERE schedule_id = %s", (schedule['id'],), fetch_one=True)
                last = res.get('last_completed') if res else None
                if isinstance(last, (str,)):
                    schedule['last_completed'] = last
                elif last:
                    schedule['last_completed'] = last.strftime('%Y-%m-%d')
                else:
                    schedule['last_completed'] = None
            except Exception:
                schedule['last_completed'] = None
        return schedules
    
    @staticmethod
    def get_by_id(schedule_id):
        """Get schedule by ID"""
        query = """
            SELECT id, equipment_id, task AS task_name, frequency, next_due, LOWER(status) as status
            FROM preventive_schedules
            WHERE id = %s
        """
        schedule = db.execute_query(query, (schedule_id,), fetch_one=True)
        if schedule:
            schedule['frequency'] = schedule.get('frequency', 'Monthly')
            try:
                res = db.execute_query("SELECT MAX(executed_on) as last_completed FROM preventive_executions WHERE schedule_id = %s", (schedule_id,), fetch_one=True)
                last = res.get('last_completed') if res else None
                if isinstance(last, (str,)):
                    schedule['last_completed'] = last
                elif last:
                    schedule['last_completed'] = last.strftime('%Y-%m-%d')
                else:
                    schedule['last_completed'] = None
            except Exception:
                schedule['last_completed'] = None
        return schedule
    
    @staticmethod
    def update(schedule_id, data):
        """Update preventive schedule"""
        query = """
            UPDATE preventive_schedules
            SET equipment_id = %s, task = %s, frequency = %s, next_due = %s, status = %s
            WHERE id = %s
        """
        asset_id = data.get('equipment_id')
        task_name = data.get('task_name')
        frequency = data.get('frequency', 'Monthly')
        next_due = data.get('next_due')
        status = data.get('status', 'Active').capitalize()

        db.execute_query(query, (asset_id, task_name, frequency, next_due, status, schedule_id), fetch_all=False)
        return PreventiveSchedule.get_by_id(schedule_id)
    
    @staticmethod
    def delete(schedule_id):
        """Delete preventive schedule"""
        query = "DELETE FROM preventive_schedules WHERE id = %s"
        db.execute_query(query, (schedule_id,), fetch_all=False)
        return True
    
    @staticmethod
    def get_by_equipment(equipment_id):
        """Get schedules for specific equipment"""
        query = """
            SELECT id, equipment_id, task AS task_name, frequency, next_due, LOWER(status) as status
            FROM preventive_schedules
            WHERE equipment_id = %s
        """
        schedules = db.execute_query(query, (equipment_id,))
        for schedule in schedules:
            schedule['frequency'] = schedule.get('frequency', 'Monthly')
            try:
                res = db.execute_query("SELECT MAX(executed_on) as last_completed FROM preventive_executions WHERE schedule_id = %s", (schedule['id'],), fetch_one=True)
                last = res.get('last_completed') if res else None
                if isinstance(last, (str,)):
                    schedule['last_completed'] = last
                elif last:
                    schedule['last_completed'] = last.strftime('%Y-%m-%d')
                else:
                    schedule['last_completed'] = None
            except Exception:
                schedule['last_completed'] = None
        return schedules
    
    @staticmethod
    def get_by_status(status):
        """Get schedules by status"""
        # status param maps to the `status` column in preventive_schedules (Active/Inactive)
        query = """
            SELECT id, equipment_id, task AS task_name, frequency, next_due, LOWER(status) as status
            FROM preventive_schedules
            WHERE LOWER(status) = %s
        """
        schedules = db.execute_query(query, (status.lower(),))
        for schedule in schedules:
            schedule['frequency'] = schedule.get('frequency', 'Monthly')
            schedule['last_completed'] = None
        return schedules
    
    @staticmethod
    def get_overdue():
        """Get overdue schedules"""
        query = """
            SELECT id, equipment_id, task AS task_name, frequency, next_due, LOWER(status) as status
            FROM preventive_schedules
            WHERE next_due < CURDATE() AND LOWER(status) != 'inactive'
        """
        schedules = db.execute_query(query)
        for schedule in schedules:
            schedule['frequency'] = schedule.get('frequency', 'Monthly')
            schedule['last_completed'] = None
            schedule['status'] = 'overdue'
        return schedules
    
    @staticmethod
    def mark_completed(schedule_id, completion_date):
        """Mark schedule as completed"""
        # Record execution and update next_due if provided
        try:
            if completion_date:
                db.execute_query("INSERT INTO preventive_executions (schedule_id, executed_on, status) VALUES (%s, %s, 'Completed')", (schedule_id, completion_date), fetch_all=False)
            # mark schedule as active (it remains), callers should update next_due separately
        except Exception:
            pass
        return PreventiveSchedule.get_by_id(schedule_id)
