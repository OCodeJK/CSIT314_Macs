from entity.Service import Service

class CleanerUpdateServiceController:
    """Controller class for handling cleaner service update operations"""
    
    def __init__(self):
        """Initialize the controller"""
        pass
    
    def cleanerUpdateService(self, serviceId, serviceName, cleanerId, categoryId):
        # Validate inputs
        if not serviceId or not serviceName or not cleanerId or not categoryId:
            print(f"Invalid input parameters: serviceId={serviceId}, serviceName={serviceName}, cleanerId={cleanerId}, categoryId={categoryId}")
            return False
            
        # Validate if category exists
        if not self.validateCategoryId(categoryId):
            print(f"Category {categoryId} does not exist in the database")
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
        
    def getServiceDetails(self, serviceId, cleanerId):

        try:
            # Get service details from entity
            service = Service.get_by_id(serviceId)
            
            if not service:
                print(f"Service {serviceId} not found")
                return None
            
            # Check if the service belongs to the cleaner
            if str(service[3]) != str(cleanerId):
                print(f"Service {serviceId} does not belong to cleaner {cleanerId}")
                return None
            
            # Format service for template
            formatted_service = {
                'serviceId': service[0],
                'serviceName': service[1],
                'categoryId': service[2],
                'cleanerId': service[3],
                'price': service[4]
            }
            
            return formatted_service
        except Exception as e:
            print(f"Error in getServiceDetails: {str(e)}")
            return None
        
    def validateCategoryId(self, categoryId):
        """Validate if the category ID exists in the database"""
        try:
            # Ensure categoryId is an integer
            try:
                # Convert to integer if it's a string
                if isinstance(categoryId, str):
                    categoryId = int(categoryId)
            except ValueError:
                print(f"Invalid category ID format: {categoryId}")
                return False
                
            # Check if the category exists
            result = Service.checkCategoryExists(categoryId)
            return result
        except Exception as e:
            print(f"Error in validateCategoryId: {str(e)}")
            return False