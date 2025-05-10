from entity.Service import Service

class HomeownerViewServiceController:
    def homeownerViewService():
        ResultSet = Service.viewServiceForHomeowner()
        return ResultSet

    def homeownerIncViewcount(serviceid):
        ResultSet = Service.incViewCount(serviceid)
        return ResultSet