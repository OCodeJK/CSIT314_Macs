from entity.HistoryRecord import HistoryRecord

class HomeownerViewCompletedServiceController:
    def homeownerViewCompletedService(userid):
        ResultSet = HistoryRecord.viewCompletedServiceForHomeowner(userid)
        return ResultSet