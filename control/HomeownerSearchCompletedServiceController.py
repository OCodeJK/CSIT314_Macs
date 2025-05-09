from entity.CompletedService import CompletedService

class HomeownerSearchCompletedServiceController:
    def homeownerSearchCompletedService(userid, service, date):
        ResultSet = CompletedService.searchCompletedServiceForHomeowner(userid, service, date)
        return ResultSet