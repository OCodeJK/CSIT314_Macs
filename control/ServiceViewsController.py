from entity.ServiceViews import ServiceViews
class ServiceViewsController:
    """Controller for service views functionality"""
    
    def getTotalViews(self, cleanerId, serviceId=None):
        return ServiceViews.getViewCount(cleanerId, serviceId)
    
    def incrementViewCount(self, serviceId):
        return ServiceViews.increment_view_count(serviceId)