from datetime import datetime, timedelta
from entity.HistoryRecord import HistoryRecord

class CleanerFilterHistoryController:

    def __init__(self):
        pass
    
    def filterHistory(self, cleanerId, startDate, endDate):

        try:
            # If both dates are None, return all history
            if not startDate and not endDate:
                return HistoryRecord.get_cleaner_history(cleanerId)
                
            # Call entity method to filter history records
            return HistoryRecord.cleanerFilterHistory(cleanerId, startDate, endDate)
        except Exception as e:
            print(f"Error in filterHistory: {str(e)}")
            return []
    
    def getHistoryDetails(self, historyId, cleanerId):

        try:
            # Directly use the method from the history_record entity
            return HistoryRecord.getHistoryDetails(historyId, cleanerId)
        except Exception as e:
            print(f"Error in getHistoryDetails: {str(e)}")
            return None