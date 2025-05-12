from entity.Shortlist import Shortlist

class ShortlistCountForCleanerController:
    """Controller for getting shortlist counts for a cleaner"""
    
    def __init__(self):
        """Initialize controller"""
        pass
    
    def getNumberOfShortlistedTime(self, cleanerId, serviceId=None):
        if not cleanerId:
            return 0
            
        # Convert to int if string
        if isinstance(cleanerId, str) and cleanerId.isdigit():
            cleanerId = int(cleanerId)
        # Convert serviceId to int if string and not None
        if serviceId and isinstance(serviceId, str) and serviceId.isdigit():
            serviceId = int(serviceId)
            
        try:
            return Shortlist.numberOfShortlistedTime(cleanerId, serviceId)
        except Exception as e:
            print(f"Error getting shortlist count: {str(e)}")
            return 0