from db_connection import ConnectionFromPool

class Service:
    def __init__(self, serviceId=None, serviceName=None, categoryId=None, cleanerId=None, price=None):
        self.serviceId = serviceId
        self.serviceName = serviceName
        self.categoryId = categoryId
        self.cleanerId = cleanerId
        self.price = price
    
    @staticmethod
    def get_all():
        with ConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM service")
            services = cursor.fetchall()
            return services
    
    @staticmethod
    def get_available_services():
        with ConnectionFromPool() as cursor:
            cursor.execute(
                """
                SELECT * FROM service 
                WHERE cleanerId IS NULL OR cleanerId = ''
                """
            )
            services = cursor.fetchall()
            return services
    
    @staticmethod
    def get_by_id(serviceId):
        with ConnectionFromPool() as cursor:
            cursor.execute(
                """
                SELECT * FROM service 
                WHERE serviceId = %s
                """,
                (serviceId,)
            )
            service = cursor.fetchone()
            return service