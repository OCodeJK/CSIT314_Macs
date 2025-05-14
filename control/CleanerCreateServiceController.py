from entity.Service import Service

class CleanerCreateServiceController:

    def cleanerCreateService(self, serviceId, cleanerId):
        result = Service.createService(serviceId, cleanerId)
        return result 