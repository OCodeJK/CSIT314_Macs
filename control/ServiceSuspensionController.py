from entity.Service import Service
from entity.HistoryRecord import HistoryRecord

class ServiceSuspensionController:
    """Controller class for handling service suspension operations"""
    
    def __init__(self):
        """Initialize the controller"""
        pass
    
    def suspendService(self, cleanerId, serviceId):

        # Validate inputs
        if not cleanerId or not serviceId:
            return False
        
        # Suspend the service using entity method
        result = Service.cleanerSuspendService(cleanerId, serviceId)
        
        return result