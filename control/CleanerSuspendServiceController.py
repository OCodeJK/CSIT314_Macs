# Fix for controller/service_suspension_controller.py
from entity.Cleaner import Cleaner
from entity.HistoryRecord import HistoryRecord

class ServiceSuspensionController:
    def __init__(self):
        self.cleaner = Cleaner()
        self.history_record = HistoryRecord()
    
    def suspendService(self, cleanerId, serviceId):
        # Validate inputs
        if not cleanerId or not serviceId:
            return False
        
        # Suspend the service
        result = self.cleaner.cleanerSuspendService(cleanerId, serviceId)
        
        # If suspension successful, update history record
        if result:
            self.history_record.end_service(cleanerId, serviceId)
        
        return result