from entity.Cleaner import Cleaner
from entity.Service import Service

class CleanerCreateServiceController:
    def __init__(self):
        self.cleaner = Cleaner()
        self.service = Service()
    
    def cleanersCreateService(self, serviceId, cleanerId):
        # Validate inputs
        if not serviceId or not cleanerId:
            return False
        
        # Check if service exists and is available
        service = self.service.get_service_by_id(serviceId)
        if not service or service[3] is not None:  # cleanerId is the 4th column (index 3)
            return False
        
        # Create the service for the cleaner
        result = self.cleaner.createService(serviceId, cleanerId)
        return result
    
    def get_available_services(self):
        # Get all services that are not assigned to any cleaner
        return self.service.get_available_services()