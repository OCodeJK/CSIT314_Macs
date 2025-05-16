from entity.Service import Service

class CleanerViewServiceController:
    """Controller class for handling cleaner service view operations"""
    
    def __init__(self):
        """Initialize the controller"""
        pass
    
    def getServiceList(self, cleanerId):
        services = Service.getServiceName(cleanerId)
        return services
    
 