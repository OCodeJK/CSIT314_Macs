from datetime import datetime
from entity.HistoryRecord import HistoryRecord

class CleanerFilterHistoryController:

    def filterHistory(self, cleanerId, startDate, endDate):
        try:
            results = HistoryRecord.cleanerFilterHistory(cleanerId, startDate, endDate)
            return results
        except Exception as e:
            print(f"Error in controller.filterHistory: {str(e)}")
            return []    
        
            