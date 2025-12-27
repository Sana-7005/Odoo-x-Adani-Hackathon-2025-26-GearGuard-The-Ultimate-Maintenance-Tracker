"""
MySQL database connection for GearGuard Admin Panel
"""

import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager

class Database:
    """MySQL database connection manager"""
    
    def __init__(self):
        self.connection_params = None
    
    def init_app(self, app):
        """Initialize database with Flask app config"""
        self.connection_params = {
            'host': app.config['DB_HOST'],
            'user': app.config['DB_USER'],
            'password': app.config['DB_PASSWORD'],
            'database': app.config['DB_NAME'],
            'port': app.config['DB_PORT'],
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        }
    
    @contextmanager
    def get_connection(self):
        """Get database connection with context manager"""
        connection = pymysql.connect(**self.connection_params)
        try:
            yield connection
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=True):
        """Execute a query and return results"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                else:
                    return cursor.lastrowid
    
    def execute_many(self, query, params_list):
        """Execute a query with multiple parameter sets"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, params_list)
                return cursor.rowcount

# Global database instance
db = Database()
