from entity.Service import Service

class CleanerUpdateServiceController:
    
    
    def cleanerUpdateService(self, serviceId, serviceName, cleanerId, categoryId):
        """Update cleaner service"""
        if not all([serviceId, serviceName, cleanerId, categoryId]):
            return False
        
        try:
            return Service.updateCleanerService(serviceId, serviceName, cleanerId, categoryId)
        except Exception:
            return False