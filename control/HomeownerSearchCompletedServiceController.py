from entity.CompletedService import CompletedService

class HomeownerSearchCompletedServiceController:
    def homeownerSearchCompletedService(userid, service): #search only
        return CompletedService.searchCompletedServiceForHomeowner(userid, service)
    def homeownerSearchCompletedServiceDateOnly(userid, date): #date only
        return CompletedService.searchCompletedServiceForHomeownerDateOnly(userid, date)
    def homeownerSearchCompletedServiceSearchNDate(userid, service, date): #search and date
        return CompletedService.searchCompletedServiceForHomeownerSearchNDate(userid, service, date)