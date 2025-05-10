from entity.Cleaner import Cleaner

class CleanerViewServiceController:
    def __init__(self):
        self.cleaner = Cleaner()
    
    def getServiceList(self, cleanerId):
        # Get the list of services for a cleaner
        services = self.cleaner.getServiceList(cleanerId)
        return services