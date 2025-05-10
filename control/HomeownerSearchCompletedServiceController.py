from entity.HistoryRecord import HistoryRecord

class HomeownerSearchCompletedServiceController:
    def homeownerSearchCompletedService(userid, service, date):
        ResultSet = HistoryRecord.searchCompletedServiceForHomeowner(userid, service, date)
        return ResultSet