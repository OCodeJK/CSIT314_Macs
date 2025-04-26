from db_connection import ConnectionFromPool
from datetime import datetime

class Cleaner:
    def __init__(self, cleanerId=None, serviceId=None, suspend_bool=None):
        self.cleanerId = cleanerId
        self.serviceId = serviceId
        self.suspend_bool = suspend_bool

    @staticmethod
    def get_all_services_for_cleaner(cleanerId):
        with ConnectionFromPool() as cursor:
            cursor.execute(
                """
                SELECT s.serviceId, s.serviceName, s.categoryId, s.cleanerId, s.price, c.suspend_bool
                FROM service s
                JOIN cleaner c ON s.cleanerId = c.cleanerId
                WHERE s.cleanerId = %s
                """,
                (cleanerId,)
            )
            services = cursor.fetchall()
            return services

    @staticmethod
    def add_service_to_cleaner(cleanerId, serviceId):
        try:
            with ConnectionFromPool() as cursor:
                # Update the service to assign it to the cleaner
                cursor.execute(
                    """
                    UPDATE service
                    SET cleanerId = %s
                    WHERE serviceId = %s AND (cleanerId IS NULL OR cleanerId = '')
                    """,
                    (cleanerId, serviceId)
                )
                # Check if service was updated
                if cursor.rowcount == 0:
                    return False
                # Create history record
                cursor.execute(
                    """
                    INSERT INTO history_record (cleanerId, serviceId, startDate)
                    VALUES (%s, %s, %s)
                    """,
                    (cleanerId, serviceId, datetime.now().date())
                )
                return True
        except Exception as e:
            print(f"Error adding service: {e}")
            return False

    @staticmethod
    def suspend_cleaner(cleanerId):
        try:
            with ConnectionFromPool() as cursor:
                # Update cleaner's suspension status
                cursor.execute(
                    """
                    UPDATE cleaner
                    SET suspend_bool = TRUE
                    WHERE cleanerId = %s
                    """,
                    (cleanerId,)
                )
                # End all active service history records for this cleaner
                cursor.execute(
                    """
                    UPDATE history_record
                    SET endDate = %s
                    WHERE cleanerId = %s AND endDate IS NULL
                    """,
                    (datetime.now().date(), cleanerId)
                )
                return True
        except Exception as e:
            print(f"Error suspending cleaner: {e}")
            return False

    @staticmethod
    def unsuspend_cleaner(cleanerId):
        try:
            with ConnectionFromPool() as cursor:
                # Update cleaner's suspension status
                cursor.execute(
                    """
                    UPDATE cleaner
                    SET suspend_bool = FALSE
                    WHERE cleanerId = %s
                    """,
                    (cleanerId,)
                )
                return True
        except Exception as e:
            print(f"Error unsuspending cleaner: {e}")
            return False
    
    @staticmethod
    def get_all_cleaners():
        with ConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM cleaner")
            cleaners = cursor.fetchall()
            
            formatted_cleaners = []
            for c in cleaners:
                formatted_cleaners.append({
                    'cleanerId': c[0],
                    'serviceId': c[1],
                    'suspend_bool': c[2]
                })
            
            return formatted_cleaners

    @staticmethod
    def get_by_id(cleanerId):
        with ConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM cleaner WHERE cleanerId = %s", (cleanerId,))
            c = cursor.fetchone()
            
            if not c:
                return None
            
            return {
                'cleanerId': c[0],
                'serviceId': c[1],
                'suspend_bool': c[2]
            }