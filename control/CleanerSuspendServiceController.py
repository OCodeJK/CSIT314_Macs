from entity.Service import Service
from entity.HistoryRecord import HistoryRecord

class ServiceSuspensionController:
    
    def suspendService(self, cleanerId, serviceId):
     
        # Validate input parameters
        if not cleanerId or not serviceId:
            return False
        # Call the Service entity method to suspend the service
        result = Service.cleanerSuspendService(cleanerId, serviceId)        
        return result