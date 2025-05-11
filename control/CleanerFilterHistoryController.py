from datetime import datetime
from entity.HistoryRecord import HistoryRecord

class CleanerFilterHistoryController:
    def __init__(self):
        pass
    
    def filterHistory(self, cleanerId, startDate, endDate):
        try:
            if not startDate and not endDate:
                return []
            
            if not startDate:
                startDate = datetime(2000, 1, 1).date()
                
            if not endDate:
                endDate = datetime.now().date()
                
            results = HistoryRecord.cleanerFilterHistory(cleanerId, startDate, endDate)
            return results
        except Exception as e:
            return []
    
    def getHistoryDetails(self, historyId, cleanerId):
        try:
            record = HistoryRecord.getHistoryDetails(historyId, cleanerId)
            return record
        except Exception as e:
            return None
            
    def endService(self, cleanerId, serviceId):
        try:
            result = HistoryRecord.end_service(cleanerId, serviceId)
            return result
        except Exception as e:
            return False