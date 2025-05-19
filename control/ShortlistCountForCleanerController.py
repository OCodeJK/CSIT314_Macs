from entity.Shortlist import Shortlist
class ShortlistCountForCleanerController:
    def getNumberOfShortlistedTime(self, cleanerId, serviceId=None): 
        try:
            return Shortlist.numberOfShortlistedTime(cleanerId, serviceId)
        except Exception:
            return 0