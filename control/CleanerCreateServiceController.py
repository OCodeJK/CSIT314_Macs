from entity.service import Service

class CleanerCreateServiceController:
    
    def __init__(self):
        pass
    
    def cleanerCreateService(self, serviceId, cleanerId):
        if not cleanerId or not serviceId:
            print(f"Invalid inputs: serviceId={serviceId}, cleanerId={cleanerId}")
            return False
        
        result = Service.createService(serviceId, cleanerId)
        
        if result:
            print(f"Successfully assigned service {serviceId} to cleaner {cleanerId}")
        else:
            print(f"Failed to assign service {serviceId} to cleaner {cleanerId}. Service may already be assigned or not available.")
            
        return result