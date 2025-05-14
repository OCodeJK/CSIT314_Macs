from entity.Service import Service
from entity.Cleaner import Cleaner

class CleanerSearchServiceController:

    def searchCleanerService(self, cleanerId, searchQuery):
        try:
            results = Service.getServices(cleanerId, searchQuery)
            return results
        except Exception as e:
            print(f"Error in searchCleanerService: {str(e)}")
            return []
    
