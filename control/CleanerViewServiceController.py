from entity.Service import Service

class CleanerViewServiceController:
    """Controller class for handling cleaner service view operations"""
    
    def __init__(self):
        """Initialize the controller"""
        pass
    
    def getServiceList(self, cleanerId):
        print(f"Getting services for cleaner {cleanerId}")
        services = Service.getServiceName(cleanerId)
        print(f"Found {len(services)} services for cleaner {cleanerId}")
        return services
    
    def getServiceById(self, serviceId):
        service = Service.get_by_id(serviceId)
        if service:
            print(f"Found service {serviceId}")
        else:
            print(f"Service {serviceId} not found")
        return service