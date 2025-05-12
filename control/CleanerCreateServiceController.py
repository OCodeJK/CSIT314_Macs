from entity.Service import Service

class CleanerCreateServiceController:
    def __init__(self):
        pass
    
    def cleanerCreateService(self, serviceId, cleanerId):
        result = Service.createService(serviceId, cleanerId)
        return result is not None

    
    def getAvailableServices(self):
        return Service.get_available_services()