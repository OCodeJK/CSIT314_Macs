from entity.HistoryRecord import HistoryRecord

class CleanerSearchHistoryController:

    def cleanerSearchService(self, searchName, cleanerId):
        try:
            if not searchName or searchName.strip() == "":
                return []
                
            results = HistoryRecord.searchService(searchName, cleanerId)
            return results
        except Exception as e:
            return []