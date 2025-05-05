from entity.CompletedService import CompletedService

class HomeownerSearchCompletedServiceController:
    def homeownerSearchCompletedService(userid, service):
        return CompletedService.searchCompletedServiceForHomeowner(userid, service)