from entity.Service import Service

class HomeownerSearchServiceController:
    def homeownerSearchService(servicename):
        ResultSet = Service.searchServiceForHomeowner(servicename)
        return ResultSet