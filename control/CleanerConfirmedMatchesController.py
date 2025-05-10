from entity.HistoryRecord import HistoryRecord

class CleanerConfirmedMatchesController:
    def __init__(self):
        pass
        
    def cleanerViewMatches(self, cleanerId: str) -> list:
        try:
            matches = HistoryRecord.cleanerVewConfirmedMatches(cleanerId)
            return matches
        except Exception:
            return []