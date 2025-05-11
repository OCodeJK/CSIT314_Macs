from entity.Service import Service
from entity.Cleaner import Cleaner

class CleanerSearchServiceController:
    def __init__(self):
        pass
    
    def searchCleanerService(self, cleanerId, searchQuery):
        try:
            results = Service.getServices(cleanerId, searchQuery)
            return results
        except Exception as e:
            print(f"Error in searchCleanerService: {str(e)}")
            return []
    
    def getCleanerInfo(self, cleanerId):
        try:
            cleaner = Cleaner.get_by_id(cleanerId)
            return cleaner
        except Exception as e:
            print(f"Error in getCleanerInfo: {str(e)}")
            return None