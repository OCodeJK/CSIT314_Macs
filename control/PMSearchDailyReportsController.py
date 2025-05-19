from entity.Reports import Report

class PMSearchDailyReportsController:
    def SearchDailyReports(self, date_str, services_name):
        return Report.SearchDailyReport(date_str, services_name)
