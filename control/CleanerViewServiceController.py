from entity.service import Service

class CleanerViewServiceController:
    """Controller class for handling cleaner service view operations"""
    
    def __init__(self):
        pass
    
    def getServiceList(self, cleanerId=None):
            return Service.getServiceName(cleanerId)