from entity.CompletedService import CompletedService

class HomeownerViewCompletedServiceController:
    def homeownerViewCompletedService(userid):
        ResultSet = CompletedService.viewCompletedServiceForHomeowner(userid)
        return ResultSet