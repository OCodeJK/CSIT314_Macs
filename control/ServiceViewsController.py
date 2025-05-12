from entity.ServiceViews import ServiceViews
from entity.Service import Service

class ServiceViewsController:
    """Controller for service views functionality"""
    
    def __init__(self):
        """Initialize controller"""
        pass
    
    def getTotalViews(self, cleanerId, serviceId=None):
        
        if not cleanerId:
            return 0
            
        if isinstance(cleanerId, str) and cleanerId.isdigit():
            cleanerId = int(cleanerId)
            
        # Convert serviceId to int if string and not None
        if serviceId and isinstance(serviceId, str) and serviceId.isdigit():
            serviceId = int(serviceId)
            
        try:
            return ServiceViews.getViewCount(cleanerId, serviceId)
        except Exception as e:
            print(f"Error getting view count: {str(e)}")
            return 0
    
    def incViewCount(self, serviceId):
        if not serviceId:
            return False
            
        if isinstance(serviceId, str) and serviceId.isdigit():
            serviceId = int(serviceId)
        try:
            return Service.incViewCount(serviceId)
        except Exception as e:
            print(f"Error incrementing view count: {str(e)}")
            return False