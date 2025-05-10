from entity.service import Service

class CleanerUpdateServiceController:
    """Controller class for handling cleaner service update operations"""
    
    def __init__(self):
        pass
    
    def cleanerUpdateService(self, serviceId, serviceName, cleanerId, categoryId):

        return Service.updateCleanerService(serviceId, serviceName, cleanerId, categoryId)
    
    