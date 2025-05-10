from entity.HistoryRecord import HistoryRecord

class CleanerSearchHistoryController:
    def __init__(self):
        pass
    
    def cleanerSearchService(self, searchName, cleanerId):
        try:
            if not searchName or searchName.strip() == "":
                # Return all cleaner history if search query is empty
                return HistoryRecord.get_cleaner_history(cleanerId)
            
            # Use the entity method directly as it now supports case-insensitive searching
            results = HistoryRecord.searchService(searchName, cleanerId)
            
            print(f"Found {len(results)} history records matching '{searchName}'")
            return results
        except Exception as e:
            print(f"Error in cleanerSearchService: {e}")
            return []
        
    def getAllHistory(self, cleanerId):

        try:
            history = HistoryRecord.getAllHistory(cleanerId)
            return history
        except Exception as e:
            print(f"Error in CleanerSearchHistoryController.getAllHistory: {e}")
            return []