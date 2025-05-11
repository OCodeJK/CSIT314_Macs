from entity.Service import Service

class CleanerViewServiceController:
    """Controller class for handling cleaner service view operations"""
    
    def __init__(self):
        """Initialize the controller"""
        pass
    
    def getServiceList(self, cleanerId=None):
  
        try:
            if not cleanerId:
                print("Warning: No cleaner ID provided")
                return []
                
            print(f"Getting services for cleaner {cleanerId}")
            services = Service.getServiceName(cleanerId)
            print(f"Found {len(services)} services for cleaner {cleanerId}")
            return services
        except Exception as e:
            print(f"Error in getServiceList: {str(e)}")
            return []
    
    def getAvailableServices(self):

        try:
            services = Service.get_available_services()
            print(f"Found {len(services)} available services")
            return services
        except Exception as e:
            print(f"Error in getAvailableServices: {str(e)}")
            return []
            
    def getServiceById(self, serviceId):

        try:
            service = Service.get_by_id(serviceId)
            if service:
                print(f"Found service {serviceId}")
            else:
                print(f"Service {serviceId} not found")
            return service
        except Exception as e:
            print(f"Error in getServiceById: {str(e)}")
            return None
