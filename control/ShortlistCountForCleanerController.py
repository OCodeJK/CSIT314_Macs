from entity.Shortlist import Shortlist

class ShortlistCountForCleanerController:

    
    def __init__(self):
        pass
    
    def getNumberOfShortlistedTime(self, cleanerId, serviceId=None):
        return Shortlist.numberOfShortlistedTime(cleanerId, serviceId)