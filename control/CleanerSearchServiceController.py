from entity.Service import Service

class CleanerSearchServiceController:
    def __init__(self):
        pass
    
    def searchCleanerService(self, cleanerId, searchQuery):
        return Service.searchServices(cleanerId, searchQuery)