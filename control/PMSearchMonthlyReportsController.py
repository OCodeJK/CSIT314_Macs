from entity.Reports import Report

class PMSearchMonthlyReportsController:
    def SearchMonthlyReports(self, year, month, services_name):
        return Report.SearchMonthlyReport(year, month, services_name)
