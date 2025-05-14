from entity.Reports import Report

class PMSearchDailyReportsController:
    def __init__(self):
        self.entity = Report()

    def SearchDailyReports(self, date_str, services_name):
        return self.entity.SearchDailyReport(date_str, services_name)
