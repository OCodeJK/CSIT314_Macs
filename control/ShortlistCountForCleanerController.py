from entity.Shortlist import Shortlist

class ShortlistCountForCleanerController:
    """
    Controller for shortlist count functionality for cleaners
    """
    
    def __init__(self):
        pass
    
    def getNumberOfShortlistedTime(self, cleanerId, serviceId):
        return Shortlist.numberOfShortlistedTime(cleanerId, serviceId)