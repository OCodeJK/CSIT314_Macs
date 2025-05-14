from entity.HistoryRecord import HistoryRecord

class CleanerViewConfirmedMatchesController:

    def cleanerViewMatches(self, cleanerId: str) -> list:
        try:
            matches = HistoryRecord.cleanerViewConfirmedMatches(cleanerId)
            return matches
        except Exception:
            return []
