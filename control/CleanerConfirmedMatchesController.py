from entity.HistoryRecord import HistoryRecord

class CleanerConfirmedMatchesController:
    def __init__(self):
        pass
        
    def cleanerViewMatches(self, cleanerId: str) -> list:
        try:
            matches = HistoryRecord.cleanerViewConfirmedMatches(cleanerId)
            return matches
        except Exception:
            return []