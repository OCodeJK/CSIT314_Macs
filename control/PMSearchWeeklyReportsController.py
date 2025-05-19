from entity.Reports import Report

class PMSearchWeeklyReportsController:
    def SearchWeeklyReports(self, year, week, services_name):
        return Report.SearchWeeklyReport(year, week, services_name)