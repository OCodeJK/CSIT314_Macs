from entity.Service import Service

class HomeownerViewServiceController:
    def homeownerViewService(serviceid):
        ResultSet = Service.viewServiceForHomeowner(serviceid)
        return  ResultSet