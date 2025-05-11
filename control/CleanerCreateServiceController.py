from entity.Service import Service

class CleanerCreateServiceController:
    def __init__(self):
        pass
    
    def cleanerCreateService(self, serviceId, cleanerId):
        result = Service.createService(serviceId, cleanerId)
        return result
    
    def getAvailableServices(self):
        try:
            return Service.get_available_services()
        except Exception as e:
            print(f"Error in getAvailableServices: {str(e)}")
            return []