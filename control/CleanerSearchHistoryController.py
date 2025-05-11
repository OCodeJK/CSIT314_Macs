from entity.HistoryRecord import HistoryRecord

class CleanerSearchHistoryController:
    def __init__(self):
        pass
    
    def cleanerSearchService(self, searchName, cleanerId):
        try:
            if not searchName or searchName.strip() == "":
                return []
                
            results = HistoryRecord.searchService(searchName, cleanerId)
            if isinstance(results, str):
                return []
            return results
        except Exception as e:
            return []