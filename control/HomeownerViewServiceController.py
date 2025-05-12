from entity.Service import Service

class HomeownerViewServiceController:
    def homeownerViewService():
        ResultSet = Service.viewServiceForHomeowner()
        return ResultSet

    def homeownerIncViewcount(serviceid):
         return Service.incViewCount(serviceid) #return true but do nothing