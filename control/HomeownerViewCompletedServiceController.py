from entity.CompletedService import CompletedService

class HomeownerViewCompletedServiceController:
    def homeownerViewCompletedService(userid):
        return CompletedService.viewCompletedServiceForHomeowner(userid)