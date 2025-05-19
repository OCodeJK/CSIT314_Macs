from entity.ServiceViews import ServiceViews

class ServiceViewsController:

    def getTotalViews(self, cleanerId, serviceId):
        try:
            return ServiceViews.getViewCount(cleanerId, serviceId)
        except Exception as e:
            print(f"Error getting view count: {str(e)}")
            return 0