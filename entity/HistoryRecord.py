from db_connection import ConnectionFromPool
from datetime import datetime

class HistoryRecord:
    def __init__(self, cleanerId=None, serviceId=None, startDate=None, endDate=None):
        self.cleanerId = cleanerId
        self.serviceId = serviceId
        self.startDate = startDate
        self.endDate = endDate
    
    @staticmethod
    def create_record(cleanerId, serviceId):
        with ConnectionFromPool() as cursor:
            cursor.execute(
                """
                INSERT INTO history_record (cleanerId, serviceId, startDate, endDate)
                VALUES (%s, %s, %s, NULL)
                """,
                (cleanerId, serviceId, datetime.now().date())
            )
            return True
    
    @staticmethod
    def end_service(cleanerId, serviceId):
        with ConnectionFromPool() as cursor:
            cursor.execute(
                """
                UPDATE history_record 
                SET endDate = %s 
                WHERE cleanerId = %s AND serviceId = %s AND endDate IS NULL
                """,
                (datetime.now().date(), cleanerId, serviceId)
            )
            return True
    
    @staticmethod
    def get_history(cleanerId):
        with ConnectionFromPool() as cursor:
            cursor.execute(
                """
                SELECT hr.*, s.serviceName 
                FROM history_record hr
                JOIN service s ON hr.serviceId = s.serviceId
                WHERE hr.cleanerId = %s
                ORDER BY hr.startDate DESC
                """,
                (cleanerId,)
            )
            history = cursor.fetchall()
            return history