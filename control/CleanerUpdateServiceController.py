from entity.Service import Service

class CleanerUpdateServiceController:
    
    
    def cleanerUpdateService(self, serviceId, serviceName, cleanerId, categoryId):
        """Update cleaner service"""
        if not serviceId or not serviceName or not cleanerId or not categoryId:
            print(f"Invalid input parameters: serviceId={serviceId}, serviceName={serviceName}, cleanerId={cleanerId}, categoryId={categoryId}")
            return False
        try:
            # Use entity method to update service
            result = Service.updateCleanerService(serviceId, serviceName, cleanerId, categoryId)
            if result:
                print(f"Service {serviceId} updated successfully")
            else:
                print(f"Failed to update service {serviceId}")
            return result
        except Exception as e:
            print(f"Error in cleanerUpdateService: {str(e)}")
            return False