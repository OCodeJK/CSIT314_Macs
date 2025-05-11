from entity.Service import Service
from entity.HistoryRecord import HistoryRecord

class ServiceSuspensionController:
    
    def __init__(self):
        self.history_record = HistoryRecord()
    
    def suspendService(self, cleanerId, serviceId):
     
        # Validate input parameters
        if not cleanerId or not serviceId:
            return False
        
        # Call the Service entity method to suspend the service
        result = Service.cleanerSuspendService(cleanerId, serviceId)
        
        # If suspension was successful, mark the service as completed in history
        if result:
            self.history_record.end_service(cleanerId, serviceId)
        
        return result